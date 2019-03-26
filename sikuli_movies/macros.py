import time
import org.sikuli.script as sikuli
import definitions as mv

def view_explorer():
    mv.send_shortcut("e", sikuli.Key.CTRL + sikuli.Key.SHIFT)


def view_extensions():
    mv.send_shortcut("v", sikuli.Key.ALT)
    button = mv.wait_image("view/extensions")
    button.click()


def view_two_columns():
    mv.send_shortcut("v", sikuli.Key.ALT)
    mv.wait_image("view/editor_layout", mv.region_vscode).click()
    mv.wait_image("view/two_columns1", mv.region_vscode).click()


LEFT = 1
RIGHT = 2


def focus_eos_ide(group=LEFT):
    mv.focus_editor_title(">EOSIde:|EOS IDE|", group)


def focus_setup(group=LEFT):
    mv.focus_editor_title(">EOSide:|Setup|", group)


def focus_install(group=LEFT):
    mv.focus_editor_title(">EOSIde:Install", group)