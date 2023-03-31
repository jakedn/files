import hash_files
import os



if __name__ == '__main__':

    ''' list of files to read the <hash>:<filename> from '''
    hash_file_names = [
        #'/mnt/x_tank/MOVING/jakedn/Nas-Maintenace/dedup.hash'
    ]

    ''' Dirs to hash and write there hash files '''
    hash_dirs = [
        #'/mnt/x_tank/APPS/NEXTCLOUD_UBUNTU/data/admin/files/SHARES/TEMP/miriams_sorting_folder/Miriams250SSD'
        #'/mnt/x_tank/MOVING/jakedn/dedup'
        #'/mnt/x_tank/APPS/NEXTCLOUD_UBUNTU/data/admin/files/SHARES/MEMORIES/jakesPictures/wax-museum',
        #'/mnt/x_tank/APPS/NEXTCLOUD_UBUNTU/data/jakedn/files/Photos/IphonePhotos',
        #'/mnt/x_tank/APPS/NEXTCLOUD_UBUNTU/data/admin/files/SHARES/TEMP/miriams_sorting_folder/Miriams250SSD/Unsorted-MEMORIES/photoesToSort'
        #'/mnt/x_tank/NEXTCLOUD_UBUNTU-daily-2022-10-09_00-00-clone/data/jakedn/files/Photos/IphonePhotos/'
        #'/mnt/x_tank/NEXTCLOUD_UBUNTU-daily-2022-10-09_00-00-clone/data/admin/files/SHARES/MEMORIES/jakesPictures/wax-museum',
        #'/mnt/x_tank/NEXTCLOUD_UBUNTU-daily-2022-10-09_00-00-clone/data/jakedn/files/Photos/IphonePhotos', 
        #'/mnt/x_tank/NEXTCLOUD_UBUNTU-daily-2022-10-09_00-00-clone/data/admin/files/SHARES/TEMP/miriams_sorting_folder/Miriams250SSD/Unsorted-MEMORIES/photoesToSort'
        '/Volumes/darktable/dedup'
    ]

    ''' dir that all of our files will be written out to '''
    write_dir = '/Volumes/darktable/dedup_output'
    # write_dir = '/mnt/x_tank/MOVING/jakedn/Nas-Maintenace/hashes'

    ''' the duplicate file name '''
    write_file_name = f'{write_dir}/dups.md'


    print('starting hash calculations')
    for hash_dir in hash_dirs:
        # check if dir exists
        if not os.path.isdir(hash_dir):
            print(f'This is not a directory skipping: {hash_dir}')
            continue

        print(f'starting dir {hash_dir}')
        file_hash_dic = hash_files.get_file_hash_dic(hash_dir)
        dir_name = hash_dir.split('/')[-1]  # take last dir name of the full path
        write_hash_file = f'{write_dir}/{dir_name}.hash'
        write_result = hash_files.write_hash_dic(file_hash_dic, write_hash_file)
        if write_result == 0:
            hash_file_names.append(write_hash_file)
            print(f'Write to {write_hash_file} finished succesfully')
        else:
            print(f'Write to {write_hash_file} failed')
    print('finished hash calculations')
    print()


    print('starting duplicate calculations')
    hash_dic = {}
    for file_name in hash_file_names:
        # check if file exists
        if not os.path.isfile(file_name):
            print(f'This is not a file skipping: {file_name}')
            continue

        # read hashes into dictionary using the write_hash_dic format
        with open(file_name, 'r') as rfile:
            data = rfile.readlines()

            for line in data:
                if line.count(':') != 1:
                    print('more then : this is bad file name!')
                    print(line)
                    print()
                    continue

                fhash, fname = line.split(':')
                if fhash in hash_dic:
                    hash_dic[fhash].append(fname)

                else:
                    hash_dic[fhash] = [fname]


    # count all duplicates and write results to a markdown file
    count_dup = 0
    with open(write_file_name, 'w') as wfile:

        for fhash in hash_dic.keys():

            if len(hash_dic[fhash]) > 1:  # meanign two files with the same hash
                wfile.write(f'# {fhash}\n')
                for i in range(len(hash_dic[fhash])):
                    numbered_line = f'{i+1}. {hash_dic[fhash][i]}\n'
                    wfile.write(numbered_line)
                wfile.write('\n')
                count_dup += 1
    print(f'finished calculating duplicates there are {count_dup} sets of duplicates')