'''
Start point:

* youyube 480 size
* open start_point folder
* view => Editor Layout => Two Columns:
    the view '|EOS IDE|' in the left,
    the file narration.md, empty, in the right one, see proper proportions
'''

'''
{
    "files.associations": {
       "functional": "cpp",
       "__config": "cpp",
       "*.ipp": "cpp"
    },
 "C_Cpp.intelliSenseEngineFallback": "Enabled",
 "workbench.activityBar.visible": false,
 "workbench.statusBar.visible": false,
 "editor.lineNumbers": "off",
 "languageTool.enabled": false,
 "cSpell.enabled": false,
 "editor.tabSize": 4,
 "editor.rulers": [120],
}

ffmpeg -i smart_contract_five_minutes.mp4 -vcodec copy -acodec copy smart_contract_five_minutes.avi

ffmpeg -loop 1 -framerate 25 -t 3 -i title.png -t 3 -f lavfi -i aevalsrc=0 -i five_minutes.mp4 -filter_complex "[0:0]fade=out:50:25:alpha=1[title]; [title][1:0][2:0][2:1] concat=n=2:v=1:a=1" five_minutes1.mp4


ffmpeg -loop 1 -t 5 -i title.png -loop 1 -t 5 -i the_end.png -f lavfi -t 5 -i anullsrc -i five_minutes.mp4 five_minutes1.mp4

'''

import os, sys, time
import shutil
import org.sikuli.script as sikuli
import definitions as mv
import macros as ma

CONTRACT_WORKSPACE = "C:\\Workspaces\\EOS\\contracts\\"
CONTRACT_NAME = "hello"
# black, blue, cyan, gray, green, magenta, orange, pink, red, white, yellow
HIGHLIGHT_COLOR = "pink" 
NAME = "smart_contract_five_minutes"

ma.view_explorer()
mv.toggle_side_bar()
build_term = mv.Terminal()
build_term.new()
mv.wait(1)
build_term.hide()
ma.focus_eos_ide(1)

narration = mv.Edit("narration")
narration.move_right()

narration.type("","w")
mv.start_ffmpeg(NAME)
mv.wait(3)

################################################################################
# Starting EOSIde
################################################################################

narration.type('''

# Starting EOSIde

With the extension 'EOSIde' enabled, this Visual Studio Code window has been launched with the command 'code -n'.
''', "w")
mv.wait(4)


################################################################################
# Get Started view
################################################################################

narration.type('''

# EOS IDE view

The view on the left can be displayed with the button '|EOS IDE|' in the 'editor title' menu.
''', "w")
mv.find(
    "file_selection\eos_ide", 
    mv.region_file_selection).highlight(3, HIGHLIGHT_COLOR)

narration.type('''
## EOS IDE view => Get Started

Live references to tutorials and other documentation. For example, the current movie can be invoked there.
''')
mv.find("eos_ide/build_first_five").highlight(4, HIGHLIGHT_COLOR)

narration.type('''
## EOS IDE view => Recent

Live references to projects created with EOSIde.
''')
mv.find("eos_ide/recent_hello").highlight(3, HIGHLIGHT_COLOR)

narration.type('''
## EOS IDE view => Open

Starts 'Select Directory' dialog.
''')
mv.find("eos_ide/open_folder").highlight(3, HIGHLIGHT_COLOR)


################################################################################
# New project
################################################################################
empty_project = mv.find("empty_project")
narration.type('''

## EOS IDE view => New Project

Creates new projects from templates. For example, the structure of empty smart-contract project.
''', "w")
empty_project.highlight(3, HIGHLIGHT_COLOR)

narration.type('''
Click the 'empty project' button.
''')

mv.delete_contract(os.path.join(CONTRACT_WORKSPACE, CONTRACT_NAME))
mv.save_all() 
empty_project.click()

mv.wait(1)

mv.open_folder(CONTRACT_NAME)
mv.wait(1)
mv.wait_image("explorer/vscode", mv.region_side_bar)
mv.set_settings(os.path.join(CONTRACT_WORKSPACE, CONTRACT_NAME))

ma.view_explorer()
mv.open_file(mv.NARRATION_FILE)
mv.wait_image("file_selection/narration", mv.region_file_selection)
mv.wait(1)
ma.view_explorer()

narration.focus_editor(1)

narration.type('''

## The layout of contract project folder.
''', "w")

narration.type('''
* '.vscode' -- EOSIde configuration files.
''')
mv.find("explorer/vscode", mv.region_side_bar).highlight(3, HIGHLIGHT_COLOR)

narration.type('''* 'build' -- contract ABIs and WASMs,
''')
mv.find("explorer/build", mv.region_side_bar).highlight(3, HIGHLIGHT_COLOR)

narration.type('''* 'resources' -- Ricardian Contract files,
''')
mv.find("explorer/resources", mv.region_side_bar).highlight(3, HIGHLIGHT_COLOR)

narration.type('''* 'src' -- contract definition files,
''')
mv.find("explorer/src", mv.region_side_bar).highlight(3, HIGHLIGHT_COLOR)

narration.type('''* 'tests' -- contract test scripts,
''')
mv.find("explorer/tests", mv.region_side_bar).highlight(3, HIGHLIGHT_COLOR)

narration.type('''* 'utils' -- helper executables.
''')
mv.find("explorer/utils", mv.region_side_bar).highlight(3, HIGHLIGHT_COLOR)

################################################################################
# Declare and define the contract
################################################################################
narration.focus_group(1)
narration.type('''
## First step: declare and define the contract.

The contract is declared in a header (.hpp) file. It is defined in a source (.cpp) file.

Write the header file.
''', "w")

if not mv.exists("explorer/hello_hpp", mv.region_side_bar):
    mv.find("explorer/src", mv.region_side_bar).click()
mv.wait_image("explorer/hello_hpp", mv.region_side_bar).click()
mv.toggle_side_bar()

narration.move_right()
narration.set_width()


################################################################################
# Edit hello_hpp
################################################################################

narration.type('''
The header includes 'eosiolib', the EOSIO smart-contract API.
''')
eosiolib = mv.find("eosiolib")
eosiolib.highlight(3, HIGHLIGHT_COLOR)

narration.type('''
The green squiggle underneath '#include' directives signal deficiencies. W can see what is missing: 
''')
eosiolib.hover()
mv.wait(5)
narration.type('''it is 'boost/limits.hpp'.

We have localized the dependency. In our system, it is 'home\\cartman\\opt\\boost\\include'.
''')


################################################################################
# Setup view
################################################################################
narration.type('''

# Setup view

This view can be displayed with the button '|Setup|' in the 'editor title' menu.
''', "w")

ma.focus_setup(1)
mv.wait(1)
mv.go_top()

narration.type('''

## Setup view => Include

Include folders, primarily the eosio.cdt defaults. 
* The entries in the list can be moved down and up, or deleted. 
* New entries can be inserted after any of the current entries. 
* The button on the left of the header adds a new entry to the end of the list.
''', "w")
mv.find("setup/include").highlight(4, HIGHLIGHT_COLOR)

narration.type('''

## Setup view => Libs

Linked libraries to be added to the eosio.cdt defaults. 
''', "w")
mv.find("setup/libs").highlight(4, HIGHLIGHT_COLOR)

narration.type('''

## Setup view => Compiler Options

Compiler options to be added to the eosio.cdt defaults.
''', "w")
mv.find("setup/options").highlight(4, HIGHLIGHT_COLOR)

narration.type('''

## Setup view => Task Buttons

Triggers for common actions:
* 'Compile' verifies the code, without producing any saved output.
* 'Build' produces ABI and WASM files.
* 'EOS IDE' opens the 'EOS IDE' view.
* 'bash' opens new terminal window.
''', "w")
mv.find("setup/buttons").highlight(4, HIGHLIGHT_COLOR)


################################################################################
# Continue with editing hello_hpp
################################################################################

narration.type('''
Add the missing include folder.
''', "w")
mv.find("setup/include").highlight(4, HIGHLIGHT_COLOR)
mv.wait_image("setup/setup_include").click()

folder_path = mv.wait_image("folder_path")
mv.type(folder_path, "home\\cartman\\opt\\boost\\include")
mv.wait(2)
mv.click("open_folder/open")

mv.close_current_editor()
hello_hpp = mv.Edit("hello.hpp")
hello_hpp.focus_editor(1)

narration.type('''
The '#include' directive is clean now.
''')

narration.type(
'''
Write declarations of the contract.
''', "w")
mv.wait(5)

hello_hpp.focus_editor()
hello_hpp.type('''
// The attribute [[eosio::contract]] is required for the 
// EOSIO.CDT ABI generator, eosio-cpp, to recognize that 
// the following class defines the contract.

''')
mv.wait(3)

hello_hpp.type('''
class [[eosio::contract("hello")]] hello : public eosio::contract {

public:
''')
mv.wait(3)

hello_hpp.type(
'''
using contract::contract;

// The attribute[[eosio::action]] will tell eosio-cpp 
// that the function is to be exposed as an action 
// for user of the smart contract.
''', end_of_file=False)
mv.wait(5)

hello_hpp.type(
'''
[[eosio::action]] void hi(eosio::name user);
''', end_of_file=False)
mv.wait(4)

hello_hpp.type(";")

mv.save_all()

narration.type('''
Write the contract definitions.
''', "w")
mv.wait(4)

mv.focus_group(1)
ma.view_explorer()
if not mv.exists("explorer/hello_cpp", mv.region_side_bar):
    mv.find("explorer/src", mv.region_side_bar).click()

mv.wait_image("explorer/hello_cpp", mv.region_side_bar).click()
mv.toggle_side_bar()

hello_cpp = mv.Edit("hello.cpp")
hello_cpp.focus_editor(1)

hello_cpp.type( 
'''
void hello::hi( eosio::name user ) {
eosio::require_auth( user );
eosio::print( "Hello, ", user);
''')
mv.wait(5)

hello_cpp.type( 
'''
// The EOSIO_DISPATCH macro to handle the dispatching 
// of actions the hello contract.
EOSIO_DISPATCH( hello, (hi))
''')
mv.wait(5)

mv.save_all()

narration.type('''
# VSCode Intelisense

See one of the wonders of VSCode, its intelisense, in action:
''', "w")

mv.hover("cpp/eosio_name")
mv.wait(4)

mv.hover("cpp/print")
mv.wait(4)

mv.hover("cpp/eosio_dispatch")
mv.wait(4)

mv.find("file_selection/narration", mv.region_file_selection).click()
require_auth = mv.find("cpp/require_auth")
require_auth.rightClick()
mv.wait_image("right_menu/pick_definition").click()
mv.wait(4)
mv.escape(require_auth)


################################################################################
# Buildind the contract
################################################################################
narration.type('''
# Build contract

EOSIde has several methods of building: one is to use buttons in the 'Setup' view. 

Here, we use the CMake style.
''', "w")
build_term.new()
build_term.type("cd build")
build_term.type("cmake ..")
build_term.type("make")

narration.focus_editor()
narration.type('''
Code files go to the 'build' folder, as usual.
''')

# for i in range(0, 5):
#     if mv.exists("terminal/built_target", mv.region_terminal):
#         print("make finished after {} period(s)".format(i))
#         break
#     time.sleep(3)

mv.wait(6)
build_term.hide()
################################################################################
# Tests
################################################################################

narration.type('''
# Test contract

Test scripts reside in the directory 'tests'. 

Write a test named 'test'.
''', "w")

mv.focus_group(1)
mv.new_file(CONTRACT_WORKSPACE + CONTRACT_NAME + "\\tests\\test.py")
test = mv.Edit("test.py")

test.type("""
import sys

from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])
CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors:
MASTER = MasterAccount()
HOST = Account()
ALICE = Account()

def test():
'''Functional test of the contract 'hello'
'''
SCENARIO('''
Execute simple actions.
''')
reset()
create_master_account("MASTER")
create_account("HOST", MASTER)
create_account("ALICE", MASTER)
""", "w")

narration.type('''
## Test stage-setting

Actors of the test:
* The account MASTER (here 'eosio') owns (creates) all other actors of the test.
''', "w")
mv.find("test/actor_master", mv.region_vscode).highlight(2, HIGHLIGHT_COLOR)

narration.type('''
* The account HOST, the owner of the contract 'hello'.
''')
mv.find("test/actor_host", mv.region_vscode).highlight(2, HIGHLIGHT_COLOR)

narration.type('''
* The account ALICE that will use the action 'hi'.
''')
mv.find("test/actor_alice", mv.region_vscode).highlight(2, HIGHLIGHT_COLOR)

narration.type('''
Start running:
* Start a local testnet, resetting everything: blockchain, wallet, ect.
''')
mv.find("test/reset", mv.region_vscode).highlight(2, HIGHLIGHT_COLOR)

narration.type('''
* Create blockchain representations of the actors: create blockchain accounts with the owner and action key, import the key to the wallet, ect. (open wallet, unlock wallet ...)
''')
mv.find("test/reset_create", mv.region_vscode).highlight(2, HIGHLIGHT_COLOR)

test.type("""
COMMENT('''
Deploy the contract:
''')
contract_hello = Contract(HOST, CONTRACT_WORKSPACE)
contract_hello.deploy()
""")

narration.type('''
Deploy the contract:

The object 'Contract' links the contract, defined with the folder 'CONTRACT_WORKSPACE' with the account 'HOST'.
''', "w")
mv.find("test/object_contract", mv.region_vscode).highlight(2, HIGHLIGHT_COLOR)

test.type("""
COMMENT('''
Test an action for ALICE:
''')
HOST.push_action(
    "hi", {"user":ALICE}, permission=(ALICE, Permission.ACTIVE)""")

test.type("""
stop()
""")

test.type(sikuli.Key.HOME + """
if __name__ == "__main__":
    test()
""")
mv.save_all()

test_term = mv.Terminal()
test_term.new()
test_term.type("cd tests")
test_term.type("python3 test.py")

for i in range(0, 5):
    if mv.exists("terminal/local_node_stopped", mv.region_terminal):
        print("make finished after {} period(s)".format(i))
        break
    time.sleep(3)

test_term.maximize()
mv.wait(2)
test_term.scroll_down(step=1)

mv.kill_ffmpeg()
