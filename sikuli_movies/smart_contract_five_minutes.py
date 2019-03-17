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
import definitions as mv

CONTRACT_WORKSPACE = "C:\\Workspaces\\EOS\\contracts"
CONTRACT_NAME = "hello"

# Starting EOSIde
mv.narration('''

# Starting EOSIde

With the VSCode extension *EOSIde* enabled, this Visual Studio Code window was launched with the command 'code -n'. 

It started with  'Get Started' view -- seen in the left-side pannel.

The left-side mv.narration panel is set to comment the action of the movie.

''', "w")
mv.wait(5)

# Get Started view
mv.narration_type('''

# EOS IDE view

This view can be desplayed with '|EOS IDE|' button in the 'editor title` menu.
''', "w")
mv.find(
    "file_selection\eos_ide", 
    mv.region_file_selection).highlight(4, "pink") # black, blue, cyan, gray, green, magenta, orange, pink, red, white, yellow

mv.narration_type('''
## Get Started

Lists active references to tutorials and documentation. For example, this movie can be invoked from its refference.
''')
mv.find("build_first_five").highlight(4, "pink")

mv.narration_type('''
## Recent

Lists active references to EOSIO smart-contract projects opened with EOSIde.
''')
mv.find("recent_hello").highlight(4, "pink")

mv.narration_type('''
## Open

The 'Open folder' button is the same as 'Open folder...' option in the VSCode Welcome view.
''')
mv.find("open_folder").highlight(4, "pink")

mv.narration_type('''
# EOS IDE view

## New Project

Creates new projects from templates. For example, EOSIde can arrange the structure of an empty smart-contract project.
''', "w")
mv.find("empty_project").highlight(4, "pink")

mv.narration_type('''
Let's click the 'empty project' button.

''')

mv.delete_contract(os.path.join(CONTRACT_WORKSPACE, CONTRACT_NAME))

mv.wait(1)
mv.save_all()
empty_project.highlight()
empty_project.click()
mv.open_folder(CONTRACT_NAME)
mv.wait(1)
mv.wait_image("explorer/vscode", mv.region_side_bar)
mv.set_settings(os.path.join(CONTRACT_WORKSPACE, CONTRACT_NAME))

mv.open_file(mv.NARRATION_FILE)
mv.wait_image("file_selection/narration", mv.region_file_selection)
mv.wait(1)
mv.narration_type('''

## The layout of a contract project folder.
''', "w")

import pdb; pdb.set_trace()
mv.narration_type('''
* '.vscode' -- EOSIde configuration files.
''')
explorer_vscode = mv.find("explorer/vscode", mv.region_side_bar)
explorer_vscode.highlight()
mv.wait(3)
explorer_vscode.highlight()

mv.narration_type('''* 'build' -- where contract ABIs and WASMs go,
''')
explorer_build = mv.find("explorer/build", mv.region_side_bar)
explorer_build.highlight()
mv.wait(3)
explorer_build.highlight()

mv.narration_type('''* 'resources' -- where Ricardian Contract files reside,
''')
explorer_resources = mv.find("explorer/resources", mv.region_side_bar)
explorer_resources.highlight()
mv.wait(3)
explorer_resources.highlight()

mv.narration_type('''* 'src' -- where contract definition files reside,
''')
explorer_src = mv.find("explorer/src", mv.region_side_bar)
explorer_src.highlight()
mv.wait(3)
explorer_src.highlight()

mv.narration_type('''* 'tests' -- where contract test scripts reside,
''')
explorer_tests = mv.find("explorer/tests", mv.region_side_bar)
explorer_tests.highlight()
mv.wait(3)
explorer_tests.highlight()

mv.narration_type('''* 'utils' -- keeps helper executables.
''')
explorer_utils = mv.find("explorer/utils", mv.region_side_bar)
explorer_utils.highlight()
mv.wait(3)
explorer_utils.highlight()

mv.narration_type('''
Adhering to this layout enables automatization features of EOSIde.
''')
mv.wait(5)


# Adjust view.
mv.narration_type('''
## First step: declare and define the smart contract

A smart contract is declared in its CPP header file, and it is defined in its source file.
Let's edit the header file.
''', "w")

if not mv.exists("explorer/hello.hpp", mv.region_side_bar):
    mv.find("explorer/src", mv.region_side_bar).click()
mv.wait_image("explorer/hello_hpp", mv.region_side_bar)
mv.region_side_bar.click(mv.region_side_bar.getLastMatch())

mv.go_to_file("narration")
mv.send_sortcut("b")
mv.click("btn_view", mv.region_menu_bar)
mv.wait_image("editor_layout", mv.region_vscode).click()
mv.wait_image("two_columns", mv.region_vscode).click()

mv.drag_drop(
    "file_selection/narration", mv.region_right_column, 
    mv.region_file_selection)

import pdb; pdb.set_trace()
## Move column border
mv.drag_drop(
    mv.find("column_border").offset(5, 0), mv.region_column_border)


# Add an include folder
mv.narration_type('''
The header includes 'eosiolib', containing the smart-contract API.
''')
eosiolib = mv.find("eosiolib")
eosiolib.highlight()
mv.wait(3)
mv.narration_type('''
The green squiggle underneath an '#include' signals a deficiency. W can see what is missing: 
''')
eosiolib.highlight()
eosiolib.hover()
mv.narration_type('''it is 'boost/limits.hpp'.

We have localized the dependency. In our system, it is 'home\\cartman\\opt\\boost\\include'.
''')
mv.click("file_selection/hello.hpp", mv.region_file_selection)
mv.wait("file_selection/setup", mv.region_file_selection).click()
mv.wait("setup_include").click()

mv.wait_image("folder_path")
mv.type(mv.region_vscode.getLastMatch(), "home\\cartman\\opt\\boost\\include")
mv.click("open_folder/open")
mv.click("file_selection/hello.hpp", mv.region_file_selection)
mv.narration_type('''
The '#include' directive is clean now.
''')


# Write hello.hpp
mv.narration_type('''
Let's write declarations of the contract.
''', "w")
mv.wait(5)
mv.edit("file_selection/hello.hpp", '''
// The attribute [[eosio::contract]] is required for the 
// EOSIO.CDT ABI generator, eosio-cpp, to recognize that 
// the following class defines the contract.
''')
mv.wait(5)
mv.edit("file_selection/hello.hpp", '''
class [[eosio::contract("hello")]] hello : public eosio::contract {
    public:
''')
mv.wait(5)
mv.edit("file_selection/hello.hpp", '''
// The attribute[[eosio::action]] will tell eosio-cpp 
// that the function is to be exposed as an action 
// for user of the smart contract.
''', end_of_file=False)
mv.wait(5)
mv.edit("file_selection/hello.hpp", '''
[[eosio::action]] void hi(eosio::name user);
''', end_of_file=False)

mv.save_all()