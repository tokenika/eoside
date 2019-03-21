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

import os, sys
import shutil
import org.sikuli.script as sikuli
import definitions as mv
import macros as ma

CONTRACT_WORKSPACE = "C:\\Workspaces\\EOS\\contracts"
CONTRACT_NAME = "hello"
# black, blue, cyan, gray, green, magenta, orange, pink, red, white, yellow
HIGHLIGHT_COLOR = "pink" 
NAME = "smart_contract_five_minutes"

narration = mv.Edit("narration")
narration.focus_editor(2)

narration.type("","w")
# mv.start_ffmpeg(NAME)

################################################################################
# Starting EOSIde
################################################################################

narration.type('''

# Starting EOSIde

With the extension 'EOSIde' enabled, this Visual Studio Code window has been launched with the command 'code -n' ('-n' option for empty 'EXPLORER').

if 'EXPLORER' is empty EOSIde starts with 'Get Started' view -- seen in the left-side pannel.

The left-side 'narration.md' panel is here just to comment the action of the movie.

''', "w")
mv.wait(5)


################################################################################
# Get Started view
################################################################################
mv.Narrator.focus()

narration.type('''

# EOS IDE view

This view can be desplayed with '|EOS IDE|' button in the 'editor title' menu.
''', "w")
mv.find(
    "file_selection\eos_ide", 
    mv.region_file_selection).highlight(4, HIGHLIGHT_COLOR)

narration.type('''
## EOS IDE view => Get Started

Lists live references to tutorials and other documentation. For example, the current movie can be invoked from one of the entries.
''')
mv.find("eos_ide/build_first_five").highlight(4, HIGHLIGHT_COLOR)

narration.type('''
## EOS IDE view => Recent

Lists live references to EOSIO smart-contract projects created with EOSIde.
''')
mv.find("eos_ide/recent_hello").highlight(4, HIGHLIGHT_COLOR)

narration.type('''
## EOS IDE view => Open

The 'Open folder...' button is the same as 'Open folder...' option in 'Welcome' view.
''')
mv.find("eos_ide/open_folder").highlight(4, HIGHLIGHT_COLOR)


################################################################################
# New project
################################################################################
empty_project = mv.find("empty_project")
narration.type('''

## EOS IDE view => New Project

Creates new projects from templates. For example, the structure of an empty smart-contract project.
''', "w")
empty_project.highlight(4, HIGHLIGHT_COLOR)

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

narration.type('''* 'build' -- where contract ABIs and WASMs go,
''')
mv.find("explorer/build", mv.region_side_bar).highlight(3, HIGHLIGHT_COLOR)

narration.type('''* 'resources' -- where Ricardian Contract files reside,
''')
mv.find("explorer/resources", mv.region_side_bar).highlight(3, HIGHLIGHT_COLOR)

narration.type('''* 'src' -- where contract definition files reside,
''')
mv.find("explorer/src", mv.region_side_bar).highlight(3, HIGHLIGHT_COLOR)

narration.type('''* 'tests' -- where contract test scripts reside,
''')
mv.find("explorer/tests", mv.region_side_bar).highlight(3, HIGHLIGHT_COLOR)

narration.type('''* 'utils' -- keeps helper executables.
''')
mv.find("explorer/utils", mv.region_side_bar).highlight(3, HIGHLIGHT_COLOR)

narration.type('''
Adhering to this standard layout enables automatization features of EOSIde.
''')
mv.wait(5)

sys.exit()
#import pdb; pdb.set_trace()
################################################################################
# Declare and define the contract
################################################################################
narration.focus_group(1)
narration.type('''
## First step: declare and define the smart contract

A smart contract is declared in its CPP header file, and it is defined in its source file.
Let's edit the header file.
''', "w")

if not mv.exists("explorer/hello_hpp", mv.region_side_bar):
    mv.find("explorer/src", mv.region_side_bar).click()
mv.wait_image("explorer/hello_hpp", mv.region_side_bar).click()
mv.toggle_side_bar()

narration.focus_editor(2)

## Move column border
mv.drag_drop(
    mv.find("column_border").offset(5, 0), mv.region_column_border)


################################################################################
# Edit hello_hpp
################################################################################

narration.type('''
The header includes 'eosiolib', containing the smart-contract API.
''')
eosiolib = mv.find("eosiolib")
eosiolib.highlight(3, HIGHLIGHT_COLOR)

narration.type('''
The green squiggle underneath an '#include' signals a deficiency. W can see what is missing: 
''')
eosiolib.hover()
mv.wait(5)
narration.type('''it is 'boost/limits.hpp'.

We have localized the dependency. In our system, it is 'home\\cartman\\opt\\boost\\include'.
''')

#import pdb; pdb.set_trace()
################################################################################
# Setup view
################################################################################
narration.type('''

# Setup view

This view can be desplayed with '|Setup|' button in the 'editor title' menu.
''', "w")

ma.select_file_to_edit("hello.hpp")

mv.find(
    "file_selection/setup", 
    mv.region_file_selection).highlight(4, HIGHLIGHT_COLOR)

mv.find("file_selection/hpp_l", mv.region_file_selection).click()
mv.wait_image("file_selection/setup").click()

narration.type('''

## Setup view => Include

Include folders, primarily the eosio.cdt default ones. The entries in the list can be moved down and up, or deleted. New entries can be inserted after any of the current entries. The insert button with the header is for adding any new entry to the end of the list.
''', "w")
mv.find("setup/include").highlight(4, HIGHLIGHT_COLOR)

narration.type('''

## Setup view => Libs

Linked libraries to be added to the eosio.cdt default ones. The entries in the list can be moved down and up, or deleted. New entries can be inserted after any of the current entries. The insert button with the header is for adding any new entry to the end of the list.
''', "w")
mv.find("setup/libs").highlight(4, HIGHLIGHT_COLOR)

narration.type('''

## Setup view => Compiler Options

Compiler options to be added to the eosio.cdt default ones. The entries in the list can be moved down and up, or deleted. New entries can be inserted after any of the current entries. The insert button with the header is for adding any new entry to the end of the list.
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

mv.find("file_selection/hpp_l", mv.region_file_selection).click()
narration.type('''
The '#include' directive is clean now.
''')

narration.type('''
Let's write declarations of the contract.
''', "w")
mv.wait(5)
mv.edit("file_selection/hpp_l", '''
// The attribute [[eosio::contract]] is required for the 
// EOSIO.CDT ABI generator, eosio-cpp, to recognize that 
// the following class defines the contract.
''')
mv.wait(5)
mv.edit("file_selection/hpp_l", '''
class [[eosio::contract("hello")]] hello : public eosio::contract {
    public:
''')
mv.wait(5)
mv.edit("file_selection/hpp_l", 
'''
// The attribute[[eosio::action]] will tell eosio-cpp 
// that the function is to be exposed as an action 
// for user of the smart contract.
''', end_of_file=False)
mv.wait(5)
mv.edit("file_selection/hpp_l", '''
[[eosio::action]] void hi(eosio::name user);
''', end_of_file=False)
mv.wait(5)

mv.save_all()

narration.type('''
Now, let's write definitions of the contract.
''', "w")
mv.wait(5)

ma.view_explorer()
if not mv.exists("explorer/hello_cpp", mv.region_side_bar):
    mv.find("explorer/src", mv.region_side_bar).click()

mv.find("file_selection/hpp_l", mv.region_file_selection).click()
mv.wait_image("explorer/hello_cpp", mv.region_side_bar).click()
ma.view_explorer()

mv.edit("file_selection/cpp_l", 
'''
void hello::hi(eosio::name user) {
   require_auth(user);
   print("Hello, ", user);
''')

mv.edit("file_selection/cpp_l", 
'''
// 'EOSIO_DISPATCH' is the macro to handle the dispatching 
// of actions for the hello contract.
EOSIO_DISPATCH( hello, (hi))
''')
mv.wait(5)

mv.save_all()

narration.type('''
# VSCode Intelisense

Let's see one of the wonders of VSCode, its intelisense, in action:
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


mv.kill_ffmpeg()
