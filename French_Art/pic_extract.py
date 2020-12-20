import zipfile
import glob, os

if __name__ == '__main__':
    done = {}
    size = len(list(glob.glob("**/*.zip", recursive=True)))
    index = 0
    for archive in glob.glob("**/*.zip", recursive=True):
        prec = int((index/size)*100)
        if prec % 5 == 0:
            if prec not in done.keys():
                print(prec, "%")
                done[prec] = prec
        try:
            directory = 'uncompressed/'
            extensions = ('.jpg', '.png', '.JPG', '.jpeg', '.JPEG', '.PNG')
            zip_file = zipfile.ZipFile(archive, 'r')
            delete_zip = False
            for file in zip_file.namelist():
                if file.endswith(extensions):
                    if not os.path.exists(directory+file):
                        zip_file.extract(file, directory)
                    else:
                        delete_zip = True
            zip_file.close()
            if delete_zip:
                print('deleting ', archive)
                os.remove(archive)
        except Exception as e:
            print(e)
            # these are easy to delete manually

        index += 1
