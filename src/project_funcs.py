# for now this is the document that contains all generic functions for this project

import os

def print_progress_bar(iteration, total, prefix='Progress:', suffix='Complete',
                       decimals=1, length=20, fill='#', print_end='\r'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


def get_file_dir_paths(directory):
    """
    Takes in a directory and returns all subdirectories and files in them.
    :param directory: top directory to start from
    :return: list of absolute file paths, list of absolute directory paths
    """

    # throw error if directory doesnt exist
    if not os.path.isdir(directory):
        raise FileNotFoundError
     
    f_names = []
    d_names = []
    #TODO if i dont have permission will walk throw error?
    for r, ds, fs in os.walk(directory):
        for d in ds:
            d_names.append(os.path.join(r, d))
        for f in fs:
            f_names.append(os.path.join(r, f))
    return f_names, d_names