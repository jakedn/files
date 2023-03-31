import sys





def read_hash_dic(hash_file):
    """
    read all hashes in the format:
    <filename>:<hash>

    and return a dictionary with filenames as keys
    """
    hash_dic = {}
    with open(hash_file, 'r') as read_file:
        for line in read_file.readlines():
            file_name, file_hash = line.split(':')
            hash_dic[file_name] = file_hash
            # check for doubles 
            if file_name in hash_dic.keys():
                print(f'there are duplicate filenames from {hash_file}')
    return hash_dic


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise Exception(f'Expecting 2 arguments got: {len(sys.argv)}')

    print()