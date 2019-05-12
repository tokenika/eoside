'''
ffmpeg -y -loop 1 -i title.png -c:v libx264 -crf 23 -pix_fmt yuv420p -pix_fmt yuv420p -movflags faststart -t 4 -framerate 25 title.mp4

ffmpeg -y -i title.mp4 -vf "fade=in:0:25,fade=out:75:25" -c:v libx264 -crf 23  -pix_fmt yuv420p -movflags faststart title_faded.mp4

ffmpeg -y -i installing_raw.mp4 -vf "fade=in:0:25" -c:v libx264 -crf 23  -pix_fmt yuv420p -movflags faststart installing_faded.mp4

concat_list.txt:
file '../header_faded.mp4'
file 'title_faded.mp4'
file 'installing_faded.mp4'
file '../final_faded.mp4'

ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy ../../../docs/_static/installing.mp4

ffplay ../../../docs/_static/installing.mp4

################################################################################


ffmpeg -i ../../../docs/_static/installing.mp4 -vcodec copy -acodec copy installing.avi
ffmpeg -i installing.mp4 -vcodec copy -acodec copy installing.avi

ffmpeg -i ../../../docs/_static/installing.mp4 -c:v libx264 -movflags +faststart ../../../docs/_static/installing1.mp4
'''

import os
import definitions as mv
import macros as ma

CONTRACT_WORKSPACE = "C:\\Workspaces\\EOS\\contracts\\"
CONTRACT_NAME = "hello1"

# black, blue, cyan, gray, green, magenta, orange, pink, red, white, yellow
HIGHLIGHT_COLOR = "pink" 
NAME = os.path.join(
                mv.sikuli_movies_dir(), "movies", "installing", "installing")
START_POINT = "movies/installing/start_point"

mv.kill_ffmpeg()
mv.delete_contract(os.path.join(CONTRACT_WORKSPACE, CONTRACT_NAME))

narration = ma.init()
mv.focus_group(1)
ma.type_setup(narration)
mv.start_ffmpeg(NAME)

mv.wait(5)
mv.show_enabled_extensions()
mv.wait(1)

extension_eoside = mv.wait_image("extension_eoside", mv.region_side_bar)
extension_eoside.highlight(3, HIGHLIGHT_COLOR)
extension_eoside.click()
mv.wait_image("logo_tokenika")
narration.move_right()
narration.type('''
# EOSIDE extends VSCode

EOSIDE is available from the VSCode Extension Marketplace.
''', "w")
extension_eoside.highlight(3, HIGHLIGHT_COLOR)
mv.toggle_side_bar()
narration.set_width()

narration.type('''

# Dependencies

* Python 3.5 or above.
* pip 3.5 or above.
* EOSFactory v3.6 or above.
* EOSIO v1.7.1.
* eosio.cdt v1.6.1.

Note: if the operating system is Windows, it has to include Windows Subsystem Linux, then all these dependencies are installed under Windows Ubuntu Bash.
''', "w")
mv.wait(4)

narration.type('''

# Installation

If all the dependencies are satisfied, EOSIDE should start ready to work, with its title bar menu.
''', "w")
mv.focus_group(1)
mv.find(
            "file_selection/title_bar_menu", 
            mv.region_file_selection
        ).highlight(3, HIGHLIGHT_COLOR)

narration.type('''

# Setting the default workspace directory

With newly installed EOSFactory, EOSIDE forces setting of the workspace.
''', "w")
mv.set_special_effects(START_POINT, [False, True])
mv.focus_group(1)
ma.install_view()
set_workspace = mv.wait_image("installing/set_workspace")
mv.set_special_effects(START_POINT)
narration.type('''
Click the button.
''')
set_workspace.click()
mv.wait(1)
mv.set_folder(mv.CONTRACT_DIR)
mv.wait_image("installing/workspaces", seconds=20, wait=3)

narration.type('''
Now, the contract workspace is set. It can be changed.
''')
mv.wait(1)
mv.wait_image("install/change_workspace").highlight(3, HIGHLIGHT_COLOR)

narration.type('''

# What if something is wrong?

The 'Install` view tries to specify a trouble. For example, it signals missing 'eosio.cdt'.
''', "w")
mv.set_special_effects(START_POINT, [True, False])
mv.focus_group(1)
ma.install_view()
mv.wait_image("installing/eosio.cdt_installed", seconds=20)
mv.set_special_effects(START_POINT)

narration.type('''
Go back to the successful installation.
''')
mv.focus_group(1)
mv.wait(1)
ma.install_view()
cdt_detected = mv.wait_image("installing/eosio.cdt_detected", seconds=20)
cdt_detected.highlight(3, HIGHLIGHT_COLOR)
narration.type('''

# Test the installation

With the 'Install' view all blue, EOSIDE should be fully functional.

Try an EOSIO smart contract. Click '|EOSIDE|' or (ctrl+alt+e with US keyboard) to open 'Get Started' view.
''', "w")
mv.wait(3)

mv.focus_group(1)
mv.wait(0.5)
ma.ide_view()

narration.type('''
Click the 'hello world' button.
''')
mv.delete_contract(os.path.join(CONTRACT_WORKSPACE, CONTRACT_NAME))
mv.save_all()

hello_world = mv.find("templates/hello_world")
hello_world.highlight(3, HIGHLIGHT_COLOR)
hello_world.click()
mv.wait(1)

mv.open_folder(CONTRACT_NAME)
mv.wait(1)
mv.wait_image("explorer/vscode", mv.region_side_bar)
mv.set_settings(
    os.path.join(CONTRACT_WORKSPACE, CONTRACT_NAME), START_POINT)

################################################################################
# Restore 'narration' file into the new VSCode folder.
# As a side-effect, Extension View appears: toggling it.
# Position the file in the right panell.
################################################################################
mv.open_file(mv.NARRATION_FILE)
mv.toggle_side_bar()
narration = mv.Edit("narration.md")
narration.move_right()
mv.wait_image("file_selection/narration", mv.region_file_selection)
mv.wait(1)

################################################################################
# Open the file 'hello.cpp'
################################################################################
ma.view_explorer()
mv.focus_group(1)
if not mv.exists("explorer/hello.cpp", mv.region_side_bar):
    mv.find("explorer/src", mv.region_side_bar).click()
    mv.hover(mv.region_menu_bar) # move cursor away

mv.wait_image("explorer/hello.cpp", mv.region_side_bar).click()
mv.toggle_side_bar()
test1 = mv.Edit("hello.cpp", 1)
test1.scroll_down(0)

################################################################################
# Build the contract
################################################################################

narration.set_width()
narration.type('''
# Build contract

EOSIDE has several methods, use CMake here.
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

narration.set_width()
narration.type('''
# Test contract

Test scripts reside in the directory 'tests'. Execute the test named 'test1.py.
''', "w")

ma.show_and_run_test("test1.py", 28, 1)

mv.wait(4)
mv.kill_ffmpeg()