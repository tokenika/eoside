# Start Windows PowerShell with the "Run as administrator" option.
# set-executionpolicy remotesigned (A)


Write-Host "
# This script, downloaded from https://github.com/tokenika/eoside,
# installs EOSIde, the Integrated Development Environment for EOSIO smart
contracts by Tokenika.
"

$workingDirectory = Convert-Path (Resolve-Path -path ".")
If(![System.IO.File]::Exists("$workingDirectory\eoside\package.json")){
    Write-Host "
# It needs to be executed from within  the 'eoside' folder. This condition 
# seems unfulfilled as the command 'dir eoside\package.json' fails.
# 
# EXITING the installer...
"
    exit    
}

Try{
    $ver=(code -v)[0]
}
Catch{
    Write-Host "
# One prerequisite is that the Visual Studio Code is installed in the System
# with its 'code' binary on the system path.
#
# The condition seems unfulfilled as the command 'code -v' fails.
#
# EXITING the installer...
"
exit
}

Try{
    $ubuntu=ubuntu run uname -a
}
Catch{
    Write-Host "
# One prerequisite is that the WLS (Windows Linux Subsystem) is installed in 
# the System.
#
# The condition seems unfulfilled as the command 
# 'ubuntu run ubuntu run uname -a' fails.
#
# EXITING the installer...
"
    exit
}

$eosfactory=ubuntu run "pip list | grep -F  eosfactory"
if(-Not $eosfactory){
    Write-Host "
# One prerequisite is that the EOSFactory Python package is installed in 
# the System.
#
# The condition seems unfulfilled as the command 
# 'ubuntu run 'pip list | grep -F  eosfactory' fails.
#
# EXITING the installer...
"
exit
}

$proceed=Read-Host "
# What about installing the EOSIde extension to the VSCode?
# It is essential for the EOSIde.
#
# Input y/n.
"
If($proceed -ne "y"){
    Write-Host "
# EXITING the installer...
"
    exit
}

# cd .\eoside\

# $vsceVersion=$vsceVersion=npm list -g vsce
# If ($vsceVersion -contains "(empty)"){
#     npm install -g vsce
# }

# Remove-Item .\*.vsix
# vsce package
# $vsixFiles=Get-ChildItem .\*.vsix

# # --install-extension (<extension-id> | <extension-vsix-path>)
# #       Installs or updates the extension. 
# #       Use `--force` argument to avoid prompts.
# code --install-extension $vsixFiles[0]

# cd ..

# Write-Host "
#          ______ ____   _____  _  _____   ______  
#         |  ____/ __ \ / ____|| ||  __ \ |  ____| 
#         | |__ | |  | | (___  | || |  | || |__
#         |  __|| |  | |\___ \ | || |  | ||  __|
#         | |___| |__| |____) || || |__| || |____ 
#         |______\____/|_____/ |_||_____/ |______| 
                                                      
# "

# Write-Host "
# To verify installation navigate to the 'eoside' folder and execute 
# 'eoside.ps1'.

# # Alternatively, run 'code -n ""'.
# # "