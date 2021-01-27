import os
import shutil


class MyFile:
    def RemoveAllFile(self,folder):
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            try:
                shutil.rmtree(filepath)
            except OSError:
                os.remove(filepath)

    def CountFile(self, folder,like):
        list = os.listdir(folder)  # dir is your directory path
        number_files = len(list)
        return number_files
