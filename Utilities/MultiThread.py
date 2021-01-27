import os
import subprocess
import time
import threading


class MultiThread(object):
    def __init__(self, num_thread=4, num_op=100):
        self.num_thread = num_thread
        self.num_op = num_op
        self.Computers = []
        assert self.num_thread > 0
        assert self.num_op > 0
        self.PsScripFile = "PowerShell\\PsScrip.ps1"
        self.MainFolder = os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\"
        self.SoftwareInventoryFolder = self.MainFolder + "\\SoftwareInventory\\"
        pass
    def SetComputers(self, Computers):
        self.Computers = Computers
    def __call__(self):
        thread_list = []
        sum =0
        for _ in range(self.num_thread):
            if sum == len(self.Computers):
                return
            t = threading.Thread(target=self.MTSoftwareInventory(self.Computers[sum]), args=(self.num_op,))
            print ("Run Computer:",sum)
            t.start()
            thread_list.append(t)
            sum += 1

        for _ in range(len(thread_list)):
            t = thread_list[_]
            t.join()

        pass

    def MTSoftwareInventory(self, computer):
        print("MTSoftwareInventory :", computer)
        param = computer.upper()
        commandline_options = 'PowerShell -noprofile -ex unrestricted -Command "& { . ' + self.PsScripFile + ' ; ' + "GetSoftwareInstalled" + ' ' + (
            param) + ' }"'
        subprocess.call(commandline_options, shell=True)
