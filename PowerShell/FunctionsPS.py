import os
import shutil
import subprocess



class FunctionsPS:
    def __init__(self):
        self.PsScripFolder = os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\ScriptPS"
        self.PsScripFile = self.PsScripFolder + "\\PsScrip.ps1"
        self.GetRemoteProgram = self.PsScripFolder + "GetRemoteProgram.ps1"
        self.Folder = os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\SoftwareInventory\\"


    def copy_and_overwrite(self, from_path, to_path):
        if os.path.exists(to_path):
            shutil.rmtree(to_path)
        shutil.copytree(from_path, to_path)

    def RunPowerShellScript(self,  function, param ):
        commandline_options = 'PowerShell -noprofile -ex unrestricted -Command "& { . ' + self.PsScripFile + ' ; ' + function  + ' ' + param + ' }"'
        print("commandline_options : ",commandline_options)
        process_result = subprocess.run(commandline_options, stdout=subprocess.PIPE, stderr=subprocess.PIPE,  universal_newlines=True)
        # PRINT RETURN CODE OF PROCESS  0 = SUCCESS, NON-ZERO = FAIL
        if process_result.returncode == 0:  # COMPARING RESULT
            return process_result.stdout
        else:
            return process_result.stderr

    def GetRSJobToLogFile(self,param):
        functionPS = "GetADComputerToJson"
        commandline_options = 'PowerShell -noprofile -ex unrestricted -Command "& { . ' + self.PsScripFile + ' ; ' + functionPS + ' ' + param + ' }"'
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

