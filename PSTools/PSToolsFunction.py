import subprocess


class PSToolsFunction:
    def EnableWinRM(self, Computers):
        for computer in Computers:
            commandPsExec = "PSTools\\PsExec.exe \\\\" +computer+ " -s c:\windows\system32\winrm.cmd quickconfig -quiet"
            print("commandPsExec:", commandPsExec)
            try :
                subprocess.call(commandPsExec, shell=True)
            except:
                print("ERROR on class PSToolsFunction -def enableWinRM ")
    def RemoveSoftwareUninstallString(self, computers, SoftwareUninstallString):
        for computer in computers:
            commandPsExec = "PSTools\\PsExec.exe \\\\" +computer+ ' -s Powershell.exe {. .\PowerShell\PsScrip.ps1; RemoveSoftwareUninstallString "'+SoftwareUninstallString+'"}'
            print("commandPsExec:", commandPsExec)
            try :
                subprocess.call(commandPsExec, shell=True)
            except:
                print("ERROR on class PSToolsFunction -def RemoveSoftwareUninstallString ")

