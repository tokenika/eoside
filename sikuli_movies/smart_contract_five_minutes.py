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
import definitions as de

CONTRACT_NAME = "hello"

de.narration_type('''

With the VSCode extension *EOSIde* is enabled, this Visual Studio Code window has been invoked with the command `code -n`, and started with the single *Get Started* view, as seen in the left-side pannel.

The left-side de.narration panel is added for the purposes of this movie.
''', "w")

de.wait(5)

de.narration_type('''

# Let us develop an EOSIO smart-contract from scratch in five minutes.

EOSIde can arrange a template empty new smart-contract project: there is the `empty project` button in the *Get Started* panel.
''', "w")

empty_project = de.region_vscode.exists(de.get_image("empty_project"))
empty_project.highlight()
de.wait(5)

de.narration_type('''

Let us click it.
''')

de.wait(1)
empty_project.highlight()
empty_project.click()
de.open_folder(CONTRACT_NAME)

de.narration_type('''

## The layout of a contract project folder.
''', "w")
open_file(de.narration_FILE)

de.narration_type('''
* '.vscode' -- EOSIde configuration files.
''')
explorer_vscode = de.find("explorer\\vscode", region_side_bar)
explorer_vscode.highlight()
de.wait(3)
explorer_vscode.highlight()

de.narration_type('''* 'build' -- where contract ABIs and WASMs go,
''')
explorer_build = de.find("explorer\\build", de.region_side_bar)
explorer_build.highlight()
de.wait(3)
explorer_build.highlight()

de.narration_type('''* 'resources' -- where Ricardian Contract files reside,
''')
explorer_resources = de.find("explorer\\resources", de.region_side_bar)
explorer_resources.highlight()
de.wait(3)
explorer_resources.highlight()

de.narration_type('''* 'src' -- where contract definition files reside,
''')
explorer_src = de.find("explorer\\src", region_side_bar)
explorer_src.highlight()
de.wait(3)
explorer_src.highlight()

de.narration_type('''* 'tests' -- where contract definition files reside,
''')
explorer_tests = de.find("explorer\\tests", region_side_bar)
explorer_tests.highlight()
de.wait(3)
explorer_tests.highlight()

de.narration_type('''* 'utils' -- where helper executables reside,
''')
explorer_utils = de.find("explorer\\utils", region_side_bar)
explorer_utils.highlight()
de.wait(3)
explorer_utils.highlight()

de.narration_type('''
We insist on adhering to this layout: it enables automatization features of EOSIde.
Also, it helps with standardization of the EOSIO smart-contract projects.
''')

de.wait(5)

de.narration_type('''
## First step: declare and define the smart contract

Typically, smart contract is declared in its CPP header file, and it is defined in its source file. Even if a simple contract can be declared and defined in a single source file, here we stick to the standard.

Let us edit the header file.
''', "w")
if not de.exists("file_selection\\hello.hpp", region_side_bar):
    explorer_src.click()
region_side_bar.de.wait(de.get_image("file_selection\\hello.hpp"))
region_side_bar.click(region_side_bar.getLastMatch())

go_to_file("de.narration_type")
send_sortcut("b")

de.region_menu_bar.click(de.get_image("btn_view"))
de.region_vscode.wait(de.get_image("editor_layout"))
de.region_vscode.click(de.region_vscode.getLastMatch())
de.region_vscode.wait(de.get_image("two_columns"))
de.region_vscode.click(de.region_vscode.getLastMatch())

column_border = de.find("column_border")
column_border.dragDrop(column_border, de.region_column_border)

de.region_menu_bar.dragDrop(de.find("file_selection\\narration"), de.region_right_column)