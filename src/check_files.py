import project_funcs
import re
import os

invalid_path_re = r'[^A-Za-z0-9_\-.' + os.path.sep + r']'
invalid_file_re = r'[^A-Za-z0-9_\-.]'

def check_file(file_name):

    dirs = file_name.split('/')
    bottom_name = dirs[len(dirs) - 1]
    return not bool(re.match(invalid_file_re, file_name))
     # look for illegal characters


def path_case_conflict(path_list_in):
    # create a dictionary to store all filenpaths with their lowercase versions as keys
    path_dict = {}
    for path in path_list_in:
        # get the lowercase version of the filename
        lowercase_path = path.lower()
        # check if this filename already exists in the dictionary
        if lowercase_path in path_dict:
            print(f"Warning: case-insensitive conflict detected: {path} and {path_dict[lowercase_path]}")
        else:
            # create empty list for the key lowercase_path
            path_dict[lowercase_path] = []

        # add path to the dictionary (we keep a record of all conflicts this way)
        path_dict[lowercase_path].append(lowercase_path)

    conflict_path_dict = {}
    for key in path_dict:
        if len(path_dict[key]) > 1:
            conflict_path_dict[key] = path_dict[key]

    return conflict_path_dict

if __name__ == '__main__':
    check_dir = input('enter a directory to search:')
    file_names, dir_names = project_funcs.get_file_dir_paths(check_dir)

    conficts = path_case_conflict(file_names)
    print(conficts)

