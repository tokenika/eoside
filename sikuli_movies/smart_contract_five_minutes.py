'''
Start point:

* youyube 480 size
* view => Editor Layout => Two Columns:
    the view '|EOS IDE|' in the left,
    the file narration.md, empty, in the right one, see proper proportions

* settings
    "workbench.activityBar.visible": false,
    "editor.lineNumbers": "off",
    "cSpell.enabled": false,


* contract folder named 'hello' deleted
'''
import org.sikuli.script as sikuli
from definitions import *

CONTRACT_NAME = "hello"

narration('''

With the VSCode extension *EOSIde* is enabled, this Visual Studio Code window has been invoked with the command `code -n`, and started with the single *Get Started* view, as seen in the left-side pannel.

The left-side narration panel is added for the purposes of this movie.
''', "w")

wait(5)

narration('''

# Let us develop an EOSIO smart-contract from scratch in five minutes.

EOSIde can arrange a template empty new smart-contract project: there is the `empty project` button in the *Get Started* panel.
''', "w")

empty_project = region_vscode.exists(get_image("empty_project"))
empty_project.highlight()
wait(5)

narration('''

Let us click it.
''', "a")

wait(1)
empty_project.highlight()
empty_project.click()
open_folder(CONTRACT_NAME)

narration('''

## The layout of a contract project folder.
''', "w")
open_file(NARRATION_FILE)

narration('''
* '.vscode' -- EOSIde configuration files.
''', "a")
explorer_vscode = region_side_bar.find(get_image("explorer_vscode"))
explorer_vscode.highlight()
wait(3)
explorer_vscode.highlight()

narration('''* 'build' -- where contract ABIs and WASMs go,
''', "a")
explorer_build = region_side_bar.find(get_image("explorer_build"))
explorer_build.highlight()
wait(3)
explorer_build.highlight()

narration('''* 'resources' -- where Ricardian Contract files reside,
''', "a")
explorer_resources = region_side_bar.find(get_image("explorer_resources"))
explorer_resources.highlight()
wait(3)
explorer_resources.highlight()

narration('''* 'src' -- where contract definition files reside,
''', "a")
explorer_src = region_side_bar.find(get_image("explorer_src"))
explorer_src.highlight()
wait(3)
explorer_src.highlight()

narration('''* 'tests' -- where contract definition files reside,
''', "a")
explorer_tests = region_side_bar.find(get_image("explorer_tests"))
explorer_tests.highlight()
wait(3)
explorer_tests.highlight()

narration('''* 'utils' -- where helper executables reside,
''', "a")
explorer_utils = region_side_bar.find(get_image("explorer_utils"))
explorer_utils.highlight()
wait(3)
explorer_utils.highlight()

narration('''
We insist on adhering to this layout: it enables automatization features of EOSIde.
Also, it helps with standardization of the EOSIO smart-contract projects.
''', "a")

wait(5)

narration('''
## First step: declare and define the smart contract

Typically, smart contract is declared in its CPP header file, here 'hello.hpp', and it is defined in its source file, here 'hello.cpp'. Even if a simple contract can be declared and defined in a single source file, here we stick to the standard.

Let us edit the header file.
''', "w")
explorer_src.click()
hello_hpp_file = region_side_bar.wait(get_image("hello_hpp_file"))
hello_hpp_file.click()


# region_vscode.wait(get_image("src_folder"))


# region_vscode.click(region_vscode.getLastMatch())
# region_vscode.wait(get_image("hello_cpp_file"))
# region_vscode.click(region_vscode.getLastMatch())

# region_vscode.type(focus_vscode, "b", sikuli.Key.CTRL)
# open_file(NARRATION_FILE)

# region_menu_bar.click(get_image("btn_view"))
# region_vscode.wait(get_image("editor_layout"))
# region_vscode.click(region_vscode.getLastMatch())
# region_vscode.wait(get_image("two_columns"))
# region_vscode.click(region_vscode.getLastMatch())
