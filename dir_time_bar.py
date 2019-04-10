import os, sys, shutil, time, datetime
from hurry.filesize import size

def check_dir(path, overwrite_bool, length, index):
    if not os.path.isdir(path):
        make_dir(path)
        printProgressBar(index, length, prefix = 'Progress:', suffix = 'Complete', length = 25)
    else:
        if not overwrite_bool:
            print(
                "The directory already exsists. Would you like to remove it before downloading? y/n")
            answer = input()
            if answer == "y":
                remove_dir(path)
                printProgressBar(index, length, prefix = 'Progress:', suffix = 'Complete', length = 25)
                make_dir(path)
                printProgressBar(index, length, prefix = 'Progress:', suffix = 'Complete', length = 25)
            else:
                sys.exit()
        else:
            remove_dir(path)
            printProgressBar(index, length, prefix = 'Progress:', suffix = 'Complete', length = 25)
            make_dir(path)
            printProgressBar(index, length, prefix = 'Progress:', suffix = 'Complete', length = 25)


def make_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)


def remove_dir(path):
    try:
        shutil.rmtree(path)
    except OSError:
        print("Removal of the directory %s failed" % path)
    else:
        print("Successfully removed the directory %s " % path)


def get_time(seconds):
    print("\nIt took " + str(datetime.timedelta(seconds=seconds))
          [:-4] + " to download the files.")


def calc_dir_size(dir_path, list_bool):
    folder_size = 0
    amount_files = 0
    for (path, dirs, files) in os.walk(dir_path):
        for file in files:
            amount_files += 1
            filename = os.path.join(path, file)
            folder_size += os.path.getsize(filename)
    if list_bool:
        return_list = [folder_size, amount_files]
        return return_list
    else:
        return_list = [size(folder_size), str(amount_files)]
        return return_list



def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
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
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total: 
        print()