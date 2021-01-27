import os

import wmi


class Network:
    def CheckOnline(self,computers):
        list=[]
        for computer in computers:
            if os.system("ping -c 1 -n 1 " + computer) == 0: # "Network Active"
                list.append(computer)
        return list
    def StartServiceWinRM(self, computers):
        serviceName = "WinRM"
        for computer in computers:
            print("computer :",computer)
            try:
                service = wmi.WMI(computer).Win32_Service(Name=serviceName)[0]
                if (service.StartMode != "Automatic"):
                    service.ChangeStartMode(StartMode="Automatic")
                    print("ChangeStartMode to Automatic")
                if service.State == "Stopped":
                    service.StartService()
                    print("StartService ")
            except:
                print(computer, " Offline")