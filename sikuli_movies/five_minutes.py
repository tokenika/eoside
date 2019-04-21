'''
Start point:

* youyube 480 size
* open start_point folder
* view => Editor Layout => Two Columns:
    the view '|EOSIDE|' in the left,
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

ffmpeg -y -loop 1 -i ..\header.png -c:v libx264 -crf 23 -pix_fmt yuv420p -pix_fmt yuv420p -movflags faststart -t 4 -framerate 25 ..\header.mp4

ffmpeg -y -i ..\header.mp4 -vf "fade=in:0:25,fade=out:75:25" -c:v libx264 -crf 23  -pix_fmt yuv420p -movflags faststart ..\header_faded.mp4

ffmpeg -y -loop 1 -i ..\final.png -c:v libx264 -crf 23 -pix_fmt yuv420p -pix_fmt yuv420p -movflags faststart -t 4 -framerate 25 ..\final.mp4

ffmpeg -y -i ..\final.mp4 -vf "fade=in:0:25,fade=out:75:25" -c:v libx264 -crf 23  -pix_fmt yuv420p -movflags faststart ..\final_faded.mp4

ffmpeg -y -loop 1 -i title.png -c:v libx264 -crf 23 -pix_fmt yuv420p -pix_fmt yuv420p -movflags faststart -t 4 -framerate 25 title.mp4

ffmpeg -y -i title.mp4 -vf "fade=in:0:25,fade=out:75:25" -c:v libx264 -crf 23  -pix_fmt yuv420p -movflags faststart title_faded.mp4

ffmpeg -y -i five_minutes_raw.mp4 -vf "fade=in:0:25" -c:v libx264 -crf 23  -pix_fmt yuv420p -movflags faststart five_minutes_faded.mp4

concat_list.txt:
file '../header_faded.mp4'
file 'title_faded.mp4'
file 'five_minutes_faded.mp4'
file '../final_faded.mp4'

ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy ../../../docs/_static/five_minutes.mp4

ffplay ../../../docs/_static/five_minutes.mp4

################################################################################

https://eosfactory.io/eoside/html/_static/installing.mp4
https://eosfactory.io/eoside/html/_static/five_minutes.mp4

ffmpeg -i ../../../docs/_static/five_minutes.mp4 -vcodec copy -acodec copy five_minutes.avi

Windows Media Player => library => File => OpenUrl... =>
https://eosfactory.io/img/five_minutes_titled.avi

Note: 'File' from right mouse library menu.

Or, better, CTRL+U
'''

import os
import org.sikuli.script as sikuli
import definitions as mv
import macros as ma

CONTRACT_WORKSPACE = "C:\\Workspaces\\EOS\\contracts\\"
CONTRACT_NAME = "hello1"
# black, blue, cyan, gray, green, magenta, orange, pink, red, white, yellow
HIGHLIGHT_COLOR = "pink"
NAME = os.path.join(
            mv.definition_dir(), "movies", "five_minutes", "five_minutes")
START_POINT = "five_minutes_start_point"

mv.kill_ffmpeg()
mv.delete_contract(os.path.join(CONTRACT_WORKSPACE, CONTRACT_NAME))

narration = ma.init()
mv.focus_group(1)
ma.ide_view()
get_started = mv.wait_image("eoside/get_started", mv.region_vscode)
if not get_started:
    print('''
Is 'EOSIDE' view focused?
Is US keyboard set?
Is 'hello' project in the 'Recent' list?
    ''')
    exit()

mv.start_ffmpeg(NAME)
mv.wait(3)

################################################################################
# Starting EOSIDE
################################################################################

narration.type('''

# Starting EOSIDE

With the extension EOSIDE enabled, this Visual Studio Code window has been launched by the command 'code -n'.
''', "w")
mv.wait(4)


################################################################################
# Get Started view
################################################################################

narration.type('''

# EOSIDE view

The view on the left can be displayed by clicking the button 'EOSIDE' in the menu, or (ctrl+alt+e).
''', "w")
mv.focus_group(1)
mv.find(
    "file_selection\eoside", 
    mv.region_file_selection).highlight(3, HIGHLIGHT_COLOR)

narration.type('''
## EOSIDE view => Get Started

Live references to tutorials and other documentation. For example, the current movie can be invoked there.
''')
mv.find("eoside/build_first_five").highlight(4, HIGHLIGHT_COLOR)

narration.type('''
## EOSIDE view => Recent

Live references to projects created with EOSIDE.
''')
mv.find("eoside/recent_hello").highlight(3, HIGHLIGHT_COLOR)

narration.type('''
## EOSIDE view => Open

Start a selection dialog.
''')
mv.find("eoside/open_folder").highlight(3, HIGHLIGHT_COLOR)


################################################################################
# New project
################################################################################
empty_project = mv.find("templates/empty_project")
narration.group = 2
narration.type('''

## EOSIDE view => New Project

Create new projects from templates. For example, the structure of empty smart-contract project.
''', "w")
empty_project.highlight(3, HIGHLIGHT_COLOR)

narration.type('''
Click the 'empty project' button.
''')

mv.save_all() 
empty_project.click()
mv.wait(1)

################################################################################
# Open the project folder.
# Set movie appearance.
################################################################################

mv.open_folder(CONTRACT_NAME)
mv.wait_image("explorer/vscode", mv.region_side_bar)

mv.set_settings(
    os.path.join(CONTRACT_WORKSPACE, CONTRACT_NAME), START_POINT)

################################################################################
# Restore 'narration' file into the new VSCode folder.
################################################################################

mv.open_file(mv.NARRATION_FILE)
mv.toggle_side_bar()
narration = mv.Edit("narration.md")
mv.wait_image("file_selection/narration", mv.region_file_selection)
mv.wait(1)
ma.view_explorer()


narration.focus_editor(1) # Sometimes focus is on Install -- if error
narration.type('''

## The layout of a contract project folder.
''', "w")

narration.type('''
* '.vscode' -- EOSIDE configuration files.
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

The contract is declared in a header file. It is defined in a source file.

Write the header file.
''', "w")

if not mv.exists("explorer/hello.hpp", mv.region_side_bar):
    mv.find("explorer/src", mv.region_side_bar).click()

mv.wait_image("explorer/hello.hpp", mv.region_side_bar).click()
mv.toggle_side_bar()

narration.move_right()
narration.set_width()


################################################################################
# Edit hello_hpp
################################################################################

narration.type('''
The header includes the eosio library, EOSIO smart-contract API.
''')
mv.wait(3)
eosiolib = mv.find("eosiolib")
eosiolib.highlight(3, HIGHLIGHT_COLOR)

narration.type('''
The green squiggle underneath #include directives signal deficiencies. W can see what is missing:
''')
eosiolib.hover()
mv.wait(5)
narration.type('''it is 'eosio.cdt/1.6.1/include/libcxx/optional' C++ source file.

We have localized the dependency. In our system, it is '/usr/opt/eosio.cdt/1.6.1/include/libcxx'.
''')


################################################################################
# Setup view
################################################################################
narration.type('''

# Setup view

This view can be displayed with the button 'Setup' in the menu, or (ctrl+alt+s).
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
* 'EOSIDE' opens the EOSIDE view.
* 'bash' opens new terminal window.
''', "w")
mv.find("setup/buttons").highlight(4, HIGHLIGHT_COLOR)


################################################################################
# Continue with editing hello_hpp
################################################################################
narration.type('''
Add the missing include folder.
''', "w")
mv.wait(1)
mv.find("setup/include").highlight(4, HIGHLIGHT_COLOR)
mv.wait_image("setup/setup_include").click()

folder_path = mv.wait_image("folder_path")
mv.type(folder_path, "usr\\opt\\eosio.cdt\\1.6.1\\include\\libcxx")
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

hello_hpp.type(
'''
class [[eosio::contract("%s")]] hello : public eosio::contract {

public:
''' % CONTRACT_NAME)
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
Write definitions of the contract.
''', "w")
mv.wait(4)

ma.view_explorer()
mv.focus_group(1)
if not mv.exists("explorer/hello.cpp", mv.region_side_bar):
    mv.find("explorer/src", mv.region_side_bar).click()

mv.wait_image("explorer/hello.cpp", mv.region_side_bar).click()
mv.toggle_side_bar()

hello_cpp = mv.Edit("hello.cpp", 1)

hello_cpp.type( 
'''
void hello::hi(eosio::name user) {
eosio::require_auth(user);
eosio::print("Hello, ", user);''')
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

mv.hover(mv.region_menu_bar)
mv.wait(0.5)
require_auth = mv.find("cpp/require_auth")
require_auth.rightClick()
mv.wait_image("right_menu/pick_definition").click()
mv.wait(4)
mv.escape(require_auth)


################################################################################
# Build the contract
################################################################################
narration.set_width()
narration.type('''
# Build contract

EOSIDE has several methods of building: one is to use buttons in the 'Setup' view. 

Here, we use the CMake style.
''', "w")
terminal = ma.cmake()

narration.focus_editor()
narration.type('''
Code files go to the 'build' folder.
''')
terminal.hide()


################################################################################
# Test
################################################################################

narration.type('''
# Test contract

Test scripts reside in the directory 'tests'. 

Write a test named 'test'.
''', "w")

mv.focus_group(1)
mv.new_file(CONTRACT_WORKSPACE + CONTRACT_NAME + "\\tests\\test.py")
test = mv.Edit("test.py")
mv.wait(1)
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

ma.run_test("test.py", 1)

mv.wait(4)
mv.kill_ffmpeg()
