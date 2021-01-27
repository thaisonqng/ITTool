import os
import subprocess



class FunctionsPS:
    def __init__(self):
        self.PsScripFile = "PowerShell\\PsScrip.ps1"
        self.GetRemoteProgram = "PowerShell\\GetRemoteProgram.ps1"
        self.Folder = os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\SoftwareInventory\\"
    def GetADComputerToJson(self,like):
        functionPS = "GetADComputerToJson"
        param = like
        commandline_options = 'PowerShell -noprofile -ex unrestricted -Command "& { . ' + self.PsScripFile + ' ; ' + functionPS + ' ' + param + ' }"'
        print("commandline_options:", commandline_options)
        subprocess.call(commandline_options, shell=True)  # , stdout=subprocess.PIPE, stderr=subprocess.STDOUT )

    def GetRSJobToLogFile(self,param):
        functionPS = "GetADComputerToJson"
        commandline_options = 'PowerShell -noprofile -ex unrestricted -Command "& { . ' + self.PsScripFile + ' ; ' + functionPS + ' ' + param + ' }"'
        subprocess.call(commandline_options, shell=True)
    def GetSoftwareInstalled(self,computers):
        param="-Computers "
        i=0
        while i < len(computers) -1 :
            param += computers[i] + "0"
            i += 1
        param += computers[len(computers)-1]
        # commandline_options = 'PowerShell -noprofile -ex unrestricted -Command "& { . ' + self.PsScripFile + ' ; ' + "GetSoftwareInstalled" + ' ' + param + ' }"'
        commandline_options = 'PowerShell -noprofile -ex unrestricted -Command "& { . ' + self.GetRemoteProgram + ' ; ' + "GetRemoteProgram" + ' ' + param + ' }"'

        subprocess.call(commandline_options, shell=True)

    def RemoveSoftware(self,computerName, software):
        param = computerName+","+software
        commandline_options = 'PowerShell -noprofile -ex unrestricted -Command "& { . ' + self.PsScripFile + ' ; ' + "RemoveSoftware" + ' ' + computerName+","+software + ' }"'
        print("commandline_options:",commandline_options)
        subprocess.call(commandline_options, shell=True)
    def RemoveSoftwareUninstallString(self,computerName, software):
        pscommand = "{Invoke-Command -ComputerName  " + computerName + " { Start-Process -FilePath  '" + software + "'   -ArgumentList '/S' -Wait }}"
        commandline_options = ' PowerShell -noprofile -ex unrestricted -Command "& { . ' + pscommand + '"  }"'
        print("commandline_options:", commandline_options)
        subprocess.call(commandline_options, shell=True)


    def RunSubprocess(self):
        command = 'PowerShell -noprofile -ex unrestricted -Command "$env:USERPROFILE"'
        process = subprocess.Popen( (command), stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print
                output.strip()
        rc = process.poll()
        return rc

