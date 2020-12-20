import glob
import os
import shutil
from random import randrange


if __name__ == '__main__':
    max_size = 300
    files = list(glob.glob("**/*.jpg"))
    size = len(files)
    index = 0
    while index < max_size:
        i = randrange(len(files)-1)
        file = files[i]
        files.remove(file)
        print(file)
        shutil.copy(file, 'some\\')
        index += 1

    print('done')
