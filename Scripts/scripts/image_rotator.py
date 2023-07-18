import os
import time
import glob
import queue
import psutil
import pathlib
import argparse
import exifread
import numpy as np
import pandas as pd
import dill as pickle
from exif import Image
import multiprocessing as mp

SENTINEL = None


def do_work(tasks_pending, tasks_completed):
    # Get the current worker's name
    worker_name = mp.current_process().name

    while True:
        try:
            task = tasks_pending.get_nowait()
        except queue.Empty:
            # print(worker_name + ' found an empty queue. Sleeping for a while before checking again...')
            time.sleep(.01)
        else:
            try:
                if task == SENTINEL:
                    # print(worker_name + ' no more work left to be done. Exiting...')
                    break

                # print(worker_name + ' received some work... ')
                time_start = time.perf_counter()
                work_func = pickle.loads(task['func'])
                # print(task['task'])
                result = work_func(**task['task'])
                tasks_completed.put({work_func.__name__: result})
                time_end = time.perf_counter() - time_start
                # print(worker_name + ' done in {} seconds'.format(round(time_end, 5)))
            except Exception as e:
                # print(worker_name + ' task failed. ' + str(e))
                tasks_completed.put({work_func.__name__: None})


def par_proc(job_list, num_cpus=None):
    # Get the number of cores
    if not num_cpus:
        num_cpus = psutil.cpu_count(logical=False) // 2

    print('* Parallel processing')
    print('* Running on {} cores'.format(num_cpus))

    # Set-up the queues for sending and receiving data to/from the workers
    tasks_pending = mp.Queue()
    tasks_completed = mp.Queue()

    # Gather processes and results here
    processes = []
    results = []

    # Count tasks
    num_tasks = 0

    # Add the tasks to the queue
    for task in job_list['tasks']:
        expanded_job = {}
        num_tasks = num_tasks + 1
        expanded_job.update({'func': pickle.dumps(job_list['func'])})
        expanded_job.update({'task': task})
        tasks_pending.put(expanded_job)

    # Use as many workers as there are cores (usually chokes the system so better use less)
    num_workers = num_cpus

    # We need as many sentinels as there are worker processes so that ALL processes exit when there is no more
    # work left to be done.
    for c in range(num_workers):
        tasks_pending.put(SENTINEL)

    print('* Number of tasks: {}'.format(num_tasks))

    # Set-up and start the workers
    for c in range(num_workers):
        p = mp.Process(target=do_work, args=(tasks_pending, tasks_completed))
        p.name = 'worker' + str(c)
        processes.append(p)
        p.start()

    # Gather the results
    completed_tasks_counter = 0
    while completed_tasks_counter < num_tasks:
        # print(tasks_completed.get())
        results.append(tasks_completed.get())
        completed_tasks_counter = completed_tasks_counter + 1

    for p in processes:
        p.join()

    return results


def rotate_img(fp):
    from exif import Image

    print(f"File Name: {fp}")

    with fp.open("rb+") as img_file:
        img = Image(img_file)
        if img.has_exif:
            img.set('orientation', 1)
        img_file.seek(0)
        img_file.write(img.get_file())
        img_file.truncate()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Image Rotator')

    parser.add_argument('--input', type=str, default="", required=True,
                        help='Input is one or more paths to input folder(s), '
                             'or a text file containing the paths to one or more input folder(s).')

    args = parser.parse_args()

    # Make it so it doesn't matter how the user provides the path
    inputs = args.input.rstrip('\\/"')

    # Make sure user added input, check against default
    if inputs == "":
        raise Exception("ERROR: No input was provided; ' \
                        please see the help for input instructions")

    # Make sure user added valid folder
    if not os.path.exists(inputs):
        raise Exception(f"ERROR: Provided input folder does not exist {inputs}")

    # Setting the root ("mother") folder
    mother_folder = inputs + "\\"

    # Globbing all jpg and JPG images
    file_paths = list(pathlib.Path(mother_folder).rglob(r"*.[jJ][pP][gG]"))

    # Looping through each of the files, adding to a queue for multiprocessing
    x = []

    for fp in file_paths:
        x.append({'fp': fp})

    # Mapping tasks in queue to function
    task_list = {'func': rotate_img, 'tasks': x}

    # Executing
    results = par_proc(task_list)

    print('done')
