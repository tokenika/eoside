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


def cmake():
    build_term = mv.Terminal()
    build_term.new()
    build_term.type("cd build")
    mv.wait(1)
    build_term.type("cmake ..")
    mv.wait(1)
    build_term.type("make")
    mv.wait_image("terminal/built_target", seconds=20, wait=3, score=0.9)


def show_and_run_test(test_name, scroll_script, scroll_result):
    view_explorer()
    mv.focus_group(1)
    if not mv.exists("explorer/{}".format(test_name)), mv.region_side_bar):
        mv.find("explorer/tests", mv.region_side_bar).click()
        mv.hover(mv.region_menu_bar) # move cursor away

    mv.wait_image("explorer/{}".format(test_name), mv.region_side_bar).click()
    mv.toggle_side_bar()
    test = mv.Edit(test_name, 1)
    test.scroll_down(scroll_script)

    terminal = mv.Terminal()
    terminal.new()
    terminal.type("cd tests")
    terminal.type("python3 {}".format(test_name))
    mv.wait_image("terminal/local_node_stopped", seconds=20, score=0.9)

    terminal.maximize()
    mv.wait(2)
    terminal.scroll_down(scroll_result)


def install_view():
    mv.region_menu_bar.type(
                    mv.region_menu_bar, "i", sikuli.Key.CTRL + sikuli.Key.ALT)


def setup_view():
    mv.region_menu_bar.type(
                    mv.region_menu_bar, "s", sikuli.Key.CTRL + sikuli.Key.ALT)

def ide_view():
    mv.region_menu_bar.type(
                    mv.region_menu_bar, "e", sikuli.Key.CTRL + sikuli.Key.ALT)
