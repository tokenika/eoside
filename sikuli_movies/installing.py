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

import os, sys, time
import shutil
import org.sikuli.script as sikuli
import definitions as mv
import macros as ma

CONTRACT_WORKSPACE = "C:\\Workspaces\\EOS\\contracts\\"
CONTRACT_NAME = "hello"
START_POINT_DIR = "C:\\Workspaces\\EOS\\eoside\\sikuli_movies\\start_point"

# black, blue, cyan, gray, green, magenta, orange, pink, red, white, yellow
HIGHLIGHT_COLOR = "pink" 
NAME = os.path.join(mv.definition_dir(), "movies", "installing", "installing")

ma.view_explorer()
mv.toggle_side_bar()

build_term = mv.Terminal()
build_term.new()
mv.wait(1)
build_term.hide()

narration = mv.Edit("narration", 2)
narration.set_width()
narration.type("","w")

mv.focus_group(1)
mv.show_enabled_extensions()
mv.wait(1)
extension_eoside = mv.wait_image("extension_eoside", mv.region_side_bar)
extension_eoside.click()
mv.wait_image("logo_tokenika")
mv.toggle_side_bar()

mv.start_ffmpeg(NAME)
mv.wait(3)

narration.type('''

# Dependencies

* If the operating system is Windows, it has to include Windows Subsystem Linux. Then, all other dependencies have to be installed under the Windows Ubuntu Bash.

* Python 3.7 or above.
* pip 3.7 or above.
* EOSFactory v3.4 or above.
* EOSIO v1.6.0 or above.
* eosio.cdt v1.5.0.
''', "w")
mv.wait(4)

narration.type('''

# Installation

If all the dependencies are satisfied and EOSFactory has the default workspace directory defined, EOSIDE should start ready to work, with its title bar menu.
''', "w")
mv.focus_group(1)
mv.find("file_selection/title_bar_menu", mv.region_file_selection).highlight(
                                                            3, HIGHLIGHT_COLOR)

narration.type('''

# Setting the default workspace directory

If all the dependencies are satisfied but with newly installed EOSFactory, 'Select Directory' dialog opens.
''', "w")

mv.set_special_effects(START_POINT_DIR, [False, True])
mv.focus_group(1)
ma.install_view()
mv.set_folder(mv.CONTRACT_DIR)
mv.set_special_effects(START_POINT_DIR)

mv.wait_image("installing/eosio.cdt_detected", seconds=20, wait=3)

narration.type('''
Now, the default contract workspace is set. It can be changed.
''')
mv.wait_image("install/change_workspace").highlight(3, HIGHLIGHT_COLOR)

narration.type('''

# What if something is wrong?

The 'Install` view tries to specify a trouble, if any. For example, it signals missing 'eosio.cdt'.
''', "w")
mv.set_special_effects(START_POINT_DIR, [True, False])
mv.focus_group(1)
ma.install_view()
mv.wait_image("installing/eosio.cdt_installed", seconds=20)
mv.set_special_effects(START_POINT_DIR)

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

Try an EOSIO smart contract. Click '|EOS IDE|' or (ctrl+alt+e with US keyboard) to open 'Get Started' view.
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
mv.set_settings(os.path.join(CONTRACT_WORKSPACE, CONTRACT_NAME))

mv.open_file(mv.NARRATION_FILE)
ma.view_explorer()
narration = mv.Edit("narration.md")
narration.move_right()
mv.wait_image("file_selection/narration", mv.region_file_selection)
mv.wait(1)

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

ma.cmake()

narration.focus_editor()
narration.type('''
Code files go to the 'build' folder.
''')
build_term.hide()


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