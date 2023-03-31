# New attempt at solving the hashing part of this project

import hashlib

def get_hash(file_name, buf_size=8192, hash_func = None):
    """
    Gets hash of specific file using no more then buf_size of ram for the hashing proccess.
    :param file_name: File to be hashed
    :param buf_size: buffer size (in bytes)
    :return: the hash value of the given function
    """

    # TODO what about the case the file doesnt exist?
    if hash_func == None:
        hash_func = hashlib.sha256()

    with open(file_name, 'rb') as file:
        data = file.read(buf_size)
        while data:
            hash_func.update(data)
            data = file.read(buf_size)
    return hash_func.hexdigest()