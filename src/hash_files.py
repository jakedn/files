import os
import threading
from queue import Queue
from hash_funcs import get_hash
import project_funcs

THREAD_AMT = 4
MAX_FILES = 50000

def thread_func(queue, dic, dic_lock):
    file_path = 'non-empty-string'
    while True:
        file_path = queue.get()

        # we added a '' to symbolize the end of the queue so that the threads actually halt
        # each thread should break after one ''
        if file_path == '':
            queue.task_done()  # this took me an hour to fix ...
            break
        file_hash = get_hash(file_path)

        # safe zone (mutually exlusive?)
        dic_lock.acquire()
        dic[file_path] = file_hash
        dic_lock.release()

        # we finished with are queue object
        queue.task_done()


def get_file_hash_dic(hashing_dir=''):
    """
    Traverses all files in the specified directory and calculates there hashes
    Retruns a dictionary of all the filename -> hash
    """
    if hashing_dir == '' or not os.path.isdir(hashing_dir):
        raise Exception(f'Directory: {hashing_dir} does not exist.')

    file_paths, dir_paths = project_funcs.get_file_dir_paths(hashing_dir)
    file_paths.sort()
    dir_paths.sort()
    if len(file_paths) >= MAX_FILES + THREAD_AMT:
        raise Exception(f'Directory {hashing_dir} has to many files for this program')

    # now create threads to hash the files
    file_path_queue = Queue(MAX_FILES)
    file_hash_dic = {}
    file_hash_dic_lock = threading.Lock()
    threads = []
    for i in range(THREAD_AMT):
        threads.append(threading.Thread(target=thread_func, args=(file_path_queue, file_hash_dic, file_hash_dic_lock, )))

    # populate queue and start the threads
    for path in file_paths:
        file_path_queue.put(path)
    for thread in threads:
        file_path_queue.put('')  # makes the thread end by itself
    for thread in threads:
        thread.daemon = True  # makes sure it gets killed when main exits
        thread.start()
    # wait till all tasks are complete and then return the dictionary
    file_path_queue.join()
    return file_hash_dic


def write_hash_dic(hash_dic, out_file):
    """
    Write all hashes to a specified file in the format:
    <hash>:<filename>
    """
    if not hash_dic:
        return -1

    # write out all hashes to file
    key_list = list(hash_dic.keys())
    key_list.sort()
    with open(out_file, 'w') as write_file:
        for key in key_list:
            write_file.write(f'{hash_dic[key]}:{key}\n')
    return 0

if __name__ == '__main__':
    calc_dir = ''  # todo find a better way to get this
    out_dir = ''  # todo find a better way to get this
    out_file_name = 'output.hash'
     # get directory from user and sort all paths
    if calc_dir == '' or not os.path.isdir(calc_dir):
        trys, max_trys = 0, 3
        while trys <= max_trys:
            calc_dir = input("Enter a directory: ")
            if os.path.isdir(calc_dir):
                break
            elif os.path.isdir(os.path.join(os.getcwd(), calc_dir)):
                calc_dir = os.path.join(os.getcwd(), calc_dir)
                break
            else:
                print("not a valid directory - try agian")
                if trys == max_trys:
                    trys += 1
                    print('maximum trials reached exiting')
                    exit(0)

    print(f'oct 8 1501 starting to hash {calc_dir}')
    hash_dic = get_file_hash_dic(calc_dir)
    write_res = write_hash_dic(hash_dic, os.path.join(out_dir, out_file_name))
    if write_res == 0:
        print(f'Success writing all hashes to {out_file_name}')
    else:
        print('Failed to write hashes no file was created.')