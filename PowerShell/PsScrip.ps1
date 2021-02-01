
Function GetADComputerToJson {
    param (
            [String]$like
        )
    $Folder=$env:USERPROFILE+"\AppData\Local\ITTool"

    get-ADComputer -Filter { Name -Like $like } | Select Name,DistinguishedName | ConvertTo-Json | Set-Content $Folder\Computers.json
}


Function RemoveSoftwareUninstallString {
        param (
        [String]$param
    )
         $computerName = $param.Split(" ")[0]
        $UninstallString = $param.Split(" ")[1]
        $UninstallString.replace("_"," ").replace("1","(1)").replace("2",")")
        Write-Host "UninstallString : $UninstallString"
        Start-Process -FilePath $UninstallString -ArgumentList '/S' -Wait
}
Function RemoveSoftwareIdentifyingNumber {
    param (
        [String]$param
    )
    $computerName = $param.Split(" ")[0]
    $id = $param.Split(" ")[1]
     Write-Host "computerName: $computerName"
     Write-Host "softwareName: $id"
    (Get-WmiObject Win32_Product -ComputerName $computerName | Where-Object {$_.IdentifyingNumber -eq "{"+$id+"}"}).Uninstall()
     $Folder = $env:USERPROFILE + "\AppData\Local\ITTool\SoftwareInventory"

}
Function GetSoftwareInstalled {
    param (
        [String]$param
    )
    $Folder = $env:USERPROFILE + "\AppData\Local\ITTool\SoftwareInventory"
    $Computers = $param.Split("0")
    foreach ($computer in $Computers) {
        Start-RSJob -Name $computer  -ArgumentList $computer, $Folder -ScriptBlock {
            $Computer = $args[0]
            $Folder = $args[1]
            $MyObject = New-Object -TypeName PSObject
            $MyObject | Add-Member @{ ComputerName = $Computer }
             if ((Test-Connection -ComputerName $Computer -Count 2 -Quiet) -eq $true){
                Try{
                    $result = Get-WmiObject Win32_product -ComputerName $Computer |select Name, Vendor, Version,IdentifyingNumber | ConvertTo-Json | Set-Content $Folder\$Computer.JSON
                    $MyObject | Add-Member @{ Status = "OK" }
                }
                catch {
                     $MyObject | Add-Member @{ Status = "ERROR" }
                }
            }
            else{
                 $MyObject | Add-Member @{ Status = "Offline" }
            }
        return $MyObject
        } #end ScriptBlock
    } #end foreach
    While (Get-RSJob "VNQN*" | ? { $_.State -eq "Running" })
	{
		Start-Sleep -Milliseconds 2000
	}
    $Result = @()
    foreach ($Job in (Get-RSJob | ? { $_.Name -like "VNQN*" }))
	{
		$JobResult = $null
		$JobResult = Receive-RSJob $Job
		$Result += $JobResult
		Stop-RSJob $Job
		Remove-RSJob $Job -Force
	}
    $Result = $Result | Select-Object -Property * -ExcludeProperty PSComputerName, RunspaceID, PSShowComputerName
    $Result    | ConvertTo-Json | Set-Content $Folder\Log.JSON

}
 Function GetRSJobToLogFile {
     param (
        [String]$name
    )
     While (Get-RSJob "$name*" | ? { $_.State -eq "Running" })
	{
         Write-Host "Still Running "
		Start-Sleep -Milliseconds 2000
	}
    $Result = @()
    foreach ($Job in (Get-RSJob | ? { $_.Name -like "name*" }))
	{
        Write-Host "Get-RSJob : $Job "

		$JobResult = $null
		$JobResult = Receive-RSJob $Job
		$Result += $JobResult
		Stop-RSJob $Job
		Remove-RSJob $Job -Force
        Write-Host "          JobResult: $JobResult "
	}
    $Result = $Result | Select-Object -Property * -ExcludeProperty PSComputerName, RunspaceID, PSShowComputerName
    $Result    | ConvertTo-Json | Set-Content $Folder\Log.JSON
     Write-Host "========> Result : $Result "
 }

Function GetRemoteProgram {
    [CmdletBinding(SupportsShouldProcess=$true)]
    param(
        [Parameter(ValueFromPipeline              =$true,
                   ValueFromPipelineByPropertyName=$true,
                   Position=0
        )]
        [string]
            $Computers = $env:COMPUTERNAME,
        [Parameter(Position=0)]
        [string[]]
             $Property=@('DisplayVersion', 'installdate', 'uninstallstring', 'installlocation'),
        [string[]]
            $IncludeProgram,
        [string[]]
            $ExcludeProgram,
        [switch]
            $ProgramRegExMatch,
        [switch]
            $LastAccessTime,
        [switch]
            $ExcludeSimilar,
        [switch]
            $DisplayRegPath,
        [switch]
            $MicrosoftStore,
        [int]
            $SimilarWord
    )

    $Folder = $env:USERPROFILE + "\AppData\Local\ITTool\SoftwareInventory"
    $ComputerName = $Computers.Split(",")
    if (Get-RSJob )
	{
		Get-RSJob   | Remove-RSJob -Force
	}
#        if ($true) {
        foreach ($Computer in $ComputerName) {
            Start-RSJob -Name "SW_$Computer" -ArgumentList $Computer -ScriptBlock {
            $Property=@('DisplayVersion', 'installdate', 'uninstallstring', 'installlocation')
            $Computer = $args[0]
#            $Result = New-Object System.Collections.ArrayList
            $Result = @()

            $Folder = $env:USERPROFILE + "\AppData\Local\ITTool\SoftwareInventory"
            $RegistryLocation = 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\',
                            'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\'

            if ($psversiontable.psversion.major -gt 2) {
                $HashProperty = [ordered]@{}
            } else {
                $HashProperty = @{}
                $SelectProperty = @('ComputerName','ProgramName')
                if ($Property) {
                    $SelectProperty += $Property
                }
                if ($LastAccessTime) {
                    $SelectProperty += 'LastAccessTime'
                }
            }
            try {
                #                    sonnt add


                 #                    sonnt add

                $socket = New-Object Net.Sockets.TcpClient($Computer, 445)
                if ($socket.Connected) {


                    'LocalMachine', 'CurrentUser' | ForEach-Object {
                        $RegName = if ('LocalMachine' -eq $_) {
                            'HKLM:\'
                        } else {
                            'HKCU:\'
                        }

                        if ($MicrosoftStore) {
                            $MSStoreRegPath = 'Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\Repository\Packages\'
                            if ('HKCU:\' -eq $RegName) {
                                if ($RegistryLocation -notcontains $MSStoreRegPath) {
                                    $RegistryLocation = $MSStoreRegPath
                                }
                            }
                        }

                        $RegBase = [Microsoft.Win32.RegistryKey]::OpenRemoteBaseKey([Microsoft.Win32.RegistryHive]::$_,$Computer)
                        $RegistryLocation | ForEach-Object {
                            $CurrentReg = $_
                            if ($RegBase) {
                                $CurrentRegKey = $RegBase.OpenSubKey($CurrentReg)
                                if ($CurrentRegKey) {
                                    $CurrentRegKey.GetSubKeyNames() | ForEach-Object {
                                        Write-Verbose -Message ('{0}{1}{2}' -f $RegName, $CurrentReg, $_)

                                        $DisplayName = ($RegBase.OpenSubKey("$CurrentReg$_")).GetValue('DisplayName')
                                        if (($DisplayName -match '^@{.*?}$') -and ($CurrentReg -eq $MSStoreRegPath)) {
                                            $DisplayName = $DisplayName  -replace '.*?\/\/(.*?)\/.*','$1'
                                        }

                                        $HashProperty.ComputerName = $Computer
                                        $HashProperty.ProgramName = $DisplayName

                                        if ($DisplayRegPath) {
                                            $HashProperty.RegPath = '{0}{1}{2}' -f $RegName, $CurrentReg, $_
                                        }

                                        if ($IncludeProgram) {
                                            if ($ProgramRegExMatch) {
                                                $IncludeProgram | ForEach-Object {
                                                    if ($DisplayName -notmatch $_) {
                                                        $DisplayName = $null
                                                    }
                                                }
                                            } else {
                                                $IncludeProgram | Where-Object {
                                                    $DisplayName -notlike ($_ -replace '\[','`[')
                                                } | ForEach-Object {
                                                    $DisplayName = $null
                                                }
                                            }
                                        }

                                        if ($ExcludeProgram) {
                                            if ($ProgramRegExMatch) {
                                                $ExcludeProgram | ForEach-Object {
                                                    if ($DisplayName -match $_) {
                                                        $DisplayName = $null
                                                    }
                                                }
                                            } else {
                                                $ExcludeProgram | Where-Object {
                                                    $DisplayName -like ($_ -replace '\[','`[')
                                                } | ForEach-Object {
                                                    $DisplayName = $null
                                                }
                                            }
                                        }

                                        if ($DisplayName) {
                                            if ($Property) {
                                                foreach ($CurrentProperty in $Property) {
                                                    $HashProperty.$CurrentProperty = ($RegBase.OpenSubKey("$CurrentReg$_")).GetValue($CurrentProperty)
                                                }
                                            }
                                            if ($LastAccessTime) {
                                                $InstallPath = ($RegBase.OpenSubKey("$CurrentReg$_")).GetValue('InstallLocation') -replace '\\$',''
                                                if ($InstallPath) {
                                                    $WmiSplat = @{
                                                        ComputerName = $Computer
                                                        Query        = $("ASSOCIATORS OF {Win32_Directory.Name='$InstallPath'} Where ResultClass = CIM_DataFile")
                                                        ErrorAction  = 'SilentlyContinue'
                                                    }
                                                    $HashProperty.LastAccessTime = Get-WmiObject @WmiSplat |
                                                            Where-Object {$_.Extension -eq 'exe' -and $_.LastAccessed} |
                                                            Sort-Object -Property LastAccessed |
                                                            Select-Object -Last 1 | ForEach-Object {
                                                                $_.ConvertToDateTime($_.LastAccessed)
                                                            }
                                                } else {
                                                    $HashProperty.LastAccessTime = $null
                                                }
                                            }

                                            if ($psversiontable.psversion.major -gt 2) {
                                                #sonnt add to list $Result
#                                                $Result.Add([pscustomobject]$HashProperty)
                                                $Result += ([pscustomobject]$HashProperty)
                                            } else {
                                                $object = New-Object -TypeName PSCustomObject -Property $HashProperty |
                                                        Select-Object -Property $SelectProperty
#                                                $Result.Add( $object)
                                                $Result  += ( $object)
                                            }
                                        }
                                        $socket.Close()
                                    }

                                }

                            }

                        } #end  $RegistryLocation | ForEach-Object
                    }
                } #end  if ($socket.Connected)

                 $MyObjectLog = New-Object -TypeName PSObject
                 $MyObjectLog | Add-Member @{ ComputerName = $Computer }
                 $MyObjectLog | Add-Member @{ Status = "OK" }
                 $Result | ConvertTo-Json | Set-Content  $Folder\$Computer.JSON

            } catch {
                if (Test-Connection -ComputerName $Computer -Count 1 -Quiet){
                     $MyObjectLog = New-Object -TypeName PSObject
                     $MyObjectLog | Add-Member @{ ComputerName = $Computer }
                     $MyObjectLog | Add-Member @{ Status = "ERROR" }
                }
                else {
                    $MyObjectLog = New-Object -TypeName PSObject
                     $MyObjectLog | Add-Member @{ ComputerName = $Computer }
                     $MyObjectLog | Add-Member @{ Status = "Offline" }
                }

                Write-Error $_
            }
        return $MyObjectLog | Select-Object -Property * -ExcludeProperty PSComputerName, RunspaceID, PSShowComputerName
        } #end ScriptBlock
        }

     $Log = @()
    do
    {
        Get-RSJob -State Completed | Foreach  {
            $RSJobResult = Receive-RSJob -Id $_.Id
            Write-Host "Receive-RSJob" $_.Name $RSJobResult
            Stop-RSJob -Id $_.Id | Out-Null
            Remove-RSJob -Id $_.Id -Force | Out-Null
            $Log += $RSJobResult
        }
        Sleep -Milliseconds 2000
    }
    while (Get-RSJob -State Running)
    $Log    | ConvertTo-Json | Set-Content $Folder\Log.JSON

}