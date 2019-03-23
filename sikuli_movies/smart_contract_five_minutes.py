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
}
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
term = mv.Terminal()
term.new()
mv.wait(1)
term.hide()
ma.focus_eos_ide(1)

narration = mv.Edit("narration")
narration.move_right()

narration.type("","w")
mv.start_ffmpeg(NAME)

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

The view on the left can be desplayed with '|EOS IDE|' button in the 'editor title' menu.
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

Starts Select Directory Dialog.
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
Let's click the 'empty project' button.
''')

mv.delete_contract(os.path.join(CONTRACT_WORKSPACE, CONTRACT_NAME))
mv.save_all() 
empty_project.click()

mv.wait(1)

mv.open_folder(CONTRACT_NAME)
mv.wait(1)
mv.wait_image("explorer/vscode", mv.region_side_bar)
mv.set_settings(os.path.join(CONTRACT_WORKSPACE, CONTRACT_NAME))

mv.open_file(mv.NARRATION_FILE)
mv.wait_image("file_selection/narration", mv.region_file_selection)
mv.wait(1)

ma.view_explorer()

narration.focus_editor(1)

narration.type('''

## The layout of a contract project folder.
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

narration.type('''
Adhering to this standard layout enhances automatization features of EOSIde.
''')
mv.wait(3)

#import pdb; pdb.set_trace()
################################################################################
# Declare and define the contract
################################################################################
narration.focus_group(1)
narration.type('''
## First step: declare and define the smart contract

The contract is declared in its header (.hpp) file. It is defined in its source (cpp) file.
Let's start with the header file.
''', "w")

if not mv.exists("explorer/hello_hpp", mv.region_side_bar):
    mv.find("explorer/src", mv.region_side_bar).click()
mv.wait_image("explorer/hello_hpp", mv.region_side_bar).click()
mv.toggle_side_bar()

narration.move_right()

## Move column border
mv.drag_drop(
    mv.find("column_border").offset(5, 0), mv.region_column_border)


################################################################################
# Edit hello_hpp
################################################################################

narration.type('''
The header includes 'eosiolib', the smart-contract API.
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

This view can be desplayed with '|Setup|' button in the 'editor title' menu.
''', "w")

ma.focus_setup(1)
mv.go_top()

narration.type('''

## Setup view => Include

Include folders, primarily the eosio.cdt default ones. 
* The entries in the list can be moved down and up, or deleted. 
* New entries can be inserted after any of the current entries. 
* The button on the left of the header adds a new entry to the end of the list.
''', "w")
mv.find("setup/include").highlight(4, HIGHLIGHT_COLOR)

narration.type('''

## Setup view => Libs

Linked libraries to be added to the eosio.cdt default ones. 
* The entries in the list can be moved down and up, or deleted. 
* New entries can be inserted after any of the current entries. 
* The button on the left of the button with the header adds a new entry to the end of the list.
''', "w")
mv.find("setup/libs").highlight(4, HIGHLIGHT_COLOR)

narration.type('''

## Setup view => Compiler Options

Compiler options to be added to the eosio.cdt default ones. 
* The entries in the list can be moved down and up, or deleted. 
* New entries can be inserted after any of the current entries. 
* The button on the left of the button with the header adds a new entry to the end of the list.
''', "w")
mv.find("setup/options").highlight(4, HIGHLIGHT_COLOR)

narration.type('''

## Setup view => Task Buttons

Triggers for common actions:
* 'Compile' compiles, without producing any saved output, in order to check the source for errors.
* 'Build' produces ABI and WASM files.
* 'EOS IDE' opens the 'EOS IDE' view.
* 'bash' opens new terminal window.
''', "w")
mv.find("setup/buttons").highlight(4, HIGHLIGHT_COLOR)


################################################################################
# Continue with editing hello_hpp
################################################################################

narration.type('''
Let's add the missing include folder.
''', "w")
mv.find("setup/include").highlight(4, HIGHLIGHT_COLOR)
mv.wait_image("setup/setup_include").click()

folder_path = mv.wait_image("folder_path")
mv.type(folder_path, "home\\cartman\\opt\\boost\\include")
mv.wait(2)
mv.click("open_folder/open")

hello_hpp = mv.Edit("hello.hpp")
hello_hpp.focus_editor(1)

narration.type('''
The '#include' directive is clean now.
''')

narration.type(
'''
Let's write declarations of the contract.
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
Now -- definitions of the contract.
''', "w")
mv.wait(4)
hello_hpp.focus_group() # to focus group for hello.cpp editor


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

term.type("cd build")
term.type("cmake ..")
term.type("make")

narration.focus_editor()
narration.type('''
Code files go to the 'build' folder, as usual.
''')

for i in range(0, 5):
    if mv.exists("terminal/built_target", mv.region_terminal):
        print("make finished after {} period(s)".format(i))
        break
    time.sleep(3)

term.hide()
################################################################################
# Tests
################################################################################

narration.type('''
# Test contract

Test scripts reside in the directory 'tests'. Let's write a test named 'test'.
''', "w")

hello_cpp.focus_group() # switch to the left group ????
mv.new_file(CONTRACT_WORKSPACE + "\\" + CONTRACT_NAME + "\\tests\\test.py")
test = mv.Edit("test.py")

test.type("""
'''
'''
import sys
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors:
MASTER = MasterAccount()
HOST = Account()
ALICE = Account()
CAROL = Account()

def test():
'''Functional test of the contract 'hello'
'''
SCENARIO('''
Execute simple actions.
''')
reset() # Start clean local testnode.
create_master_account("MASTER") # Master account (here 'eosio') owns (creates) all other actors of the test.

COMMENT('''
Build and deploy the contract:
''')
create_account("HOST", MASTER) 
contract_hello = Contract(HOST, CONTRACT_WORKSPACE) # The actor HOST owns the contract defined and built in the current project -- 'CONTRACT_WORKSPACE' is the link to the project.
contract_hello.deploy()

""")

test.type("""
'''
'''
import sys
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors:
MASTER = MasterAccount()
HOST = Account()
ALICE = Account()
CAROL = Account()

def test():
    '''Functional test of the contract 'hello'
    '''
    SCENARIO('''
    Execute simple actions.
    ''')
    reset() # Start clean local testnode.
    create_master_account("MASTER") # Master account (here 'eosio') owns (creates) all other actors of the test.

    COMMENT('''
    Build and deploy the contract:
    ''')
    create_account("HOST", MASTER) 
    contract_hello = Contract(HOST, CONTRACT_WORKSPACE) # The actor HOST owns the contract defined and built in the current project -- 'CONTRACT_WORKSPACE' is the link to the project.
    contract_hello.deploy()

    COMMENT('''
    Create test accounts:
    ''')
    create_account("ALICE", MASTER)
    create_account("CAROL", MASTER)

    COMMENT('''
    Test an action for ALICE:
    ''')
    HOST.push_action(
        "hi", {"user":ALICE}, permission=(ALICE, Permission.ACTIVE))
    assert("ALICE" in DEBUG())

    COMMENT('''
    Test an action for CAROL:
    ''')
    HOST.push_action(
        "hi", {"user":CAROL}, permission=(CAROL, Permission.ACTIVE))
    assert("CAROL" in DEBUG())

    stop()


if __name__ == "__main__":
    test()
""")

mv.kill_ffmpeg()



# def goto_top():
#     region_menu_bar.type(region_menu_bar, sikuli.Key.HOME, sikuli.Key.CTRL)


# mv.region_vscode.type(mv.region_vscode, sikuli.Key.HOME, sikuli.Key.CTRL)
# for i in range(0, 50):
#     mv.region_vscode.wheel(mv.region_vscode, sikuli.Button.WHEEL_DOWN, 1)
#     # time.sleep(0.5)

# mv.region_vscode.type(mv.region_vscode, sikuli.Key.SPACE, sikuli.Key.ALT)
# mv.region_vscode.type("n")
