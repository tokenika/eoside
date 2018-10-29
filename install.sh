#!/bin/bash

printf "%s\n" "
###############################################################################
#   This script installs EOSIde. It needs to be executed from within 
#   the 'eoside' folder.
#   This file was downloaded from https://github.com/tokenika/eoside
###############################################################################
"

python3 -c "$(cat <<'END'
import importlib

if importlib.util.find_spec("eosfactory"):
    print("EOSFactory package is already installed in the system.")
else:
    print('''
EOSFactory python package, downloaded from https://github.com/tokenika/eoside",
has to be installed in order to make EOSIde productive.
''')
END
)"

printf "%s" "
Installing the 'eoside' package locally with the Python pip system...
"

###############################################################################
# It is essentioal that the package is installed as a symlink, with 
# the flag '-e'
###############################################################################
sudo  -H python3 -m pip install -e .

txtbld=$(tput bold)
bldred=${txtbld}$(tput setaf 1)
txtrst=$(tput sgr0)
printf "${bldred}%s${txtrst}" '
         ______ ____   _____  _  _____   ______  
        |  ____/ __ \ / ____|| ||  __ \ |  ____| 
        | |__ | |  | | (___  | || |  | || |__
        |  __|| |  | |\___ \ | || |  | ||  __|
        | |___| |__| |____) || || |__| || |____ 
        |______\____/|_____/ |_||_____/ |______| 
                                                      
'
printf "%s\n" "
To verify EOSide installation navigate to the 'eoside' folder and run 
these tests:
"
printf "%s\n" "    
    $ python3 tests/01_hello_world.py
    $ python3 tests/02_eosio_token.py
    $ python3 tests/03_tic_tac_toe.py
"