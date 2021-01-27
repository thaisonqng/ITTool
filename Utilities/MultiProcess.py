import os
import subprocess
import time
from multiprocessing import Process

class MultiProcess(object):
    def __init__(self, num_process=4, num_op=100):
        print("MultiProcess __init__")
        self.num_process = num_process
        self.num_op = num_op
        self.param = ""
        self.Computers = []
        self.PsScripFile = "PowerShell\\PsScrip.ps1"
        self.MainFolder = os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\"
        self.SoftwareInventoryFolder = self.MainFolder + "\\SoftwareInventory\\"
        assert self.num_process > 0
        assert self.num_op > 0
        pass
    def __call__(self):
        print("MultiProcess __call__")
        process_list = []
        sum = len(self.Computers)
        for i in range(self.num_process):
            for j in range(sum // self.num_process):
                current= i*(self.num_process + j)
                if (current == sum):
                    print("RETURN")
                    return
                else:
                    print("RUn current :", current)
                    p = Process(target=self.MPSoftwareInventory(self.Computers[current]), args=(self.num_op,))
                    p.start()
                    process_list.append(p)


        for _ in range(len(process_list)):
            p = process_list[_]
            p.join()

        pass

    def SetComputers(self, Computers):
        self.Computers = Computers
    def MPSoftwareInventory(self,computer):
        print("MPSoftwareInventory :",computer)
        param = computer.upper()
        commandline_options = 'PowerShell -noprofile -ex unrestricted -Command "& { . ' + self.PsScripFile + ' ; ' + "GetSoftwareInstalled" + ' ' + (
            param) + ' }"'
        subprocess.call(commandline_options, shell=True)

