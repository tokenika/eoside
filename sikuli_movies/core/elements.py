import sys
import time
import org.sikuli.script as sikuli
import definitions as de
    

# def view_two_columns():
#     print("         [SIKULI MOVIES] view_two_columns()")
#     de.send_shortcut("v", sikuli.Key.ALT)
#     de.wait_image("view/editor_layout", de.REGION_VSCODE).click()
#     de.wait_image("view/two_columns", de.REGION_VSCODE).click() asorted


def show_shortcut_view(
    detector, key, ctrl, begin_msg=None,
    PS=None, region=de.REGION_VSCODE, seconds=3, wait=0, score=0, 
    module_level=3):

    if not PS:
        PS = detector

    begin_msg = begin_msg if begin_msg else ""
    begin_msg = begin_msg + ", return region '{}':".format(PS) \
                                    if not PS == detector else begin_msg + "."

    function_name = de.ACTION(begin_msg, module_level)
    de.FOCUS_VSCODE.type(de.FOCUS_VSCODE, key, ctrl)

    print "{} waits for {}".format(function_name, PS),
    sys.stdout.flush()

    detected1 = de.wait_image(detector, seconds=20)
    detected = detected1 if PS == detector else de.wait_image(
                                            PS, region, seconds, wait, score)
    de.CUT(module_level)

    if PS == detector:
        return
    
    return detected


def show_enabled_extensions(
                PS=None, region=de.REGION_VSCODE, seconds=3, wait=0, score=0):
    return show_shortcut_view(
        "view/enabled_extension",
        "xe", sikuli.Key.CTRL + sikuli.Key.SHIFT,
        "Show enabled extensions", 
        PS, region, seconds, wait, score)


def show_explorer(
                PS=None, region=de.REGION_VSCODE, seconds=3, wait=0, score=0):
    return show_shortcut_view(
        "view/explorer",
        "e", sikuli.Key.CTRL + sikuli.Key.SHIFT,
        None,
        PS, region, seconds, wait, score)


def maximize_editor_group():
    de.ACTION()

    de.FOCUS_VSCODE.type(
                    de.FOCUS_VSCODE, "q", sikuli.Key.CTRL + sikuli.Key.ALT)
    de.wait(1)

    region_side_margin = sikuli.Region(de.X, de.Y, 10, de.H)
    side_margin_empty = de.exists("side_margin_empty", region_side_margin)
    if side_margin_empty and side_margin_empty.getScore > 0.9:
        de.CUT()
    else:
        de.exit('''
Cannot hide the side bar.
        ''')


def hide_side_bar():
    de.ACTION()

    region_detector = sikuli.Region(de.X, de.Y + 25, 120, 30)
    images = [
        de.get_image("hide_side_bar/explorer"), 
        de.get_image("hide_side_bar/extensions"),
        de.get_image("hide_side_bar/debug"),
        de.get_image("hide_side_bar/search"),
        de.get_image("hide_side_bar/scm")
        ]
    detector = region_detector.findAny(images)
    if detector:
        print("Toggling the Side Bar.")
        de.FOCUS_VSCODE.type(de.FOCUS_VSCODE, "b", sikuli.Key.CTRL)
        de.wait(1)
        if not region_detector.exists(detector[0].getImageFilename()):
            de.CUT()
        else:
            de.exit('''
Cannot hide the side bar.
            ''')


def close_all_editors():
    de.ACTION()
    region_top_margin = sikuli.Region(de.X, de.Y + 20, de.W, 30)
    side_margin_empty = de.exists("top_margin_empty", region_top_margin)
    if side_margin_empty and side_margin_empty.getScore > 0.9:
        de.CUT()

    de.FOCUS_VSCODE.type(de.FOCUS_VSCODE, "kw", sikuli.Key.CTRL)
    de.wait(1)

    side_margin_empty = de.exists("top_margin_empty", region_top_margin)
    if side_margin_empty and side_margin_empty.getScore > 0.9:
        de.CUT()
    else:
        de.exit('''
Cannot close editors.
        ''')


def ok_keyboard():
    eng_us = de.exists("eng_us", sikuli.Screen(0))
    if not (eng_us and eng_us.getScore() >= 0.9):
        raise Exception("ERROR: Set keybord to ENG US")


def type_setup(narration):
    de.ACTION()
    narration.focus()
    narration.type(de.SETUP, "w")
    de.CUT()


def show_terminal(                
                PS=None, region=de.REGION_VSCODE, seconds=3, wait=0, score=0):
    return show_shortcut_view(
        "terminal/TERMINAL",
        "jf", sikuli.Key.CTRL + sikuli.Key.SHIFT,
        None,
        PS, region, seconds, wait, score)


def hide_terminal_panel():
    de.ACTION()
    de.FOCUS_VSCODE.type(
                    de.FOCUS_VSCODE, "jc", sikuli.Key.CTRL + sikuli.Key.SHIFT)
    de.wait(1)
    if de.exists("terminal/TERMINAL"):
        de.exit('''
Cannot hide the terminal panel.
        ''')
    de.CUT()


def new_bash_terminal(                
                PS=None, region=de.REGION_VSCODE, seconds=3, wait=0, score=0):
    return show_shortcut_view(
        "terminal/TERMINAL",
        "x", sikuli.Key.CTRL + sikuli.Key.ALT,
        None,
        PS, region, seconds, wait, score)