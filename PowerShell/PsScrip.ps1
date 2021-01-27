
Function GetADComputerToJson {
    param (
            [String]$like
        )
#    $ListOnline = @()
#    $Listoffline = @()
    $Folder=$env:USERPROFILE+"\AppData\Local\ITTool"

    get-ADComputer -Filter { Name -Like $like } | Select Name,DistinguishedName | ConvertTo-Json | Set-Content $Folder\Computers.json
#    if ((Test-Connection -ComputerName (get-ADComputer -Filter { Name -Like $like } | Select Name) -Count 2 -Quiet) -eq $true){
#
#
#    }
}

Function GetADComputerToJson1 {
    param (
            [String]$like
        )
#    $ListOnline = @()
#    $Listoffline = @()
    $Folder=$env:USERPROFILE+"\AppData\Local\ITTool\SoftwareInventory"
    $Result =  get-ADComputer -Filter { Name -Like $like } | Select Name,DistinguishedName
    $Result | ConvertTo-Json | Set-Content $Folder\Computers.json
    return $Result
#    if ((Test-Connection -ComputerName (get-ADComputer -Filter { Name -Like $like } | Select Name) -Count 2 -Quiet) -eq $true){
#
#
#    }
}
Function RemoveSoftwareUninstallString1 {
        param (
        [String]$param
    )

         $computerName = $param.Split(",")[0]
        $UninstallString = $param.Split(",")[1]
          Write-Host "param : $param"
          Write-Host "computerName : $computerName"
          Write-Host "UninstallString : $UninstallString"
        Invoke-Command -ComputerName $computerName -ScriptBlock {Start-Process -FilePath $UninstallString -ArgumentList '/S' -Wait}
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
#    $sw = Get-WmiObject Win32_Product -ComputerName $ComputerName | Where-Object {$_.IdentifyingNumber -eq $id}
#     Write-Host "$sw"
#    if ($sw) {
#      $sw.Uninstall()
#      "OK" | ConvertTo-Json | Set-Content $Folder\LogRemoveSW.JSON
#      return $true
#    }
#    else {
#      Write-Host "$sw is not installed on   $ComputerName"
#      "FAIL" | ConvertTo-Json | Set-Content $Folder\LogRemoveSW.JSON
#      return $false
#    }
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