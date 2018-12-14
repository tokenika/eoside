# Start Windows PowerShell with the "Run as administrator" option.
# set-executionpolicy remotesigned (A)


Write-Host "
# This script, downloaded from https://github.com/tokenika/eoside,
# installs EOSIde, the Integrated Development Environment for EOSIO smart
contracts by Tokenika.
"

Write-Host "Checking the current directory ..."
$workingDirectory = Convert-Path (Resolve-Path -path ".")
If(![System.IO.File]::Exists("$workingDirectory\package.json")){
    Write-Host "
# It needs to be executed from within  the 'eoside' folder. This condition 
# seems unfulfilled as the command 'dir eoside\package.json' fails.
# 
# EXITING the installer...
"
    exit    
}

Write-Host "Checking whether the Visual Studio Code is installed ..."
Try{
    $ver=(code -v)[0]
}
Catch{
    Write-Host "
# One prerequisite is that the Visual Studio Code is installed in the System
# with its 'code' binary on the system path.
#
# The condition seems unfulfilled as the command 'code -v' fails. See
# https://code.visualstudio.com/
#
# EXITING the installer...
"
exit
}

Write-Host "Checking whether the Windows Linux Subsystem is installed ..."
Try{
    $ubuntu=ubuntu run uname -a
}
Catch{
    Write-Host "
# One prerequisite is that the WLS (Windows Linux Subsystem) is installed in 
# the System.
#
# The condition seems unfulfilled as the command 
# 'ubuntu run ubuntu run uname -a' fails. See
# https://docs.microsoft.com/en-us/windows/wsl/install-win10
#
# EXITING the installer...
"
    exit
}

Write-Host "Checking whether the EOSFactory Python package is available ..."
$eosfactory=ubuntu run "pip list | grep -F  eosfactory"
if(-Not $eosfactory){
    Write-Host "
# One prerequisite is that the EOSFactory Python package is installed in 
# the System.
#
# The condition seems unfulfilled as the command 
# 'ubuntu run 'pip list | grep -F  eosfactory' fails. See
# https://github.com/tokenika/eosfactory
#
# EXITING the installer...
"
exit
}

$root=""
Write-Host "
Checking configuration of the EOSFactory Python package ...
"
$Lxss="hkcu\Software\Microsoft\Windows\CurrentVersion\Lxss"
$basePath=REG QUERY $Lxss  -s -v BasePath
If($basePath){
    $x=$basePath[2] -match 'REG_SZ\s*(.*)'
    If($basePath[2] -match 'REG_SZ\s*(.*)'){
        $root=$matches[1]
        $root="$root\rootfs"
        $user=ubuntu run whoami
        $bashrc=""
        $bashrc=Get-ChildItem -Path "${root}\home\${user}\.bashrc" -Name
        
        If($bashrc -And $bashrc -eq ".bashrc"){
            Write-Host "
WSL root directory is
$root

    "
        }
    }
}

$vsceVersion=$vsceVersion=npm list -g vsce
If ($vsceVersion -contains "(empty)"){
    npm install -g vsce
}

Remove-Item .\*.vsix
vsce package
$vsixFiles=Get-ChildItem .\*.vsix

# --install-extension (<extension-id> | <extension-vsix-path>)
#       Installs or updates the extension. 
#       Use `--force` argument to avoid prompts.
code --install-extension $vsixFiles[0]

cd ..

Write-Host "
         ______   ____    _____  _  _____   ______  
        |  ____| / __ \  / ____|| ||  __ \ |  ____| 
        | |__   | |  | || (___  | || |  | || |__
        |  __|  | |  | | \___ \ | || |  | ||  __|
        | |___  | |__| | ____) || || |__| || |____ 
        |______| \____/ |_____/ |_||_____/ |______| 
                                                      
"

Write-Host "
To verify installation navigate to the 'eoside' folder and execute 
'eoside.ps1'.

# Alternatively, run 'code -n'.
# "