import sys
import os
import time
import org.sikuli.script as sikuli

VSCODE = "eosfactory - Visual Studio Code"
NARRATION_FILE = "C:\\Workspaces\\EOS\\eoside\\sikuli_movies\\narration.md"
CONTRACT_DIR = "C:\\Workspaces\\EOS\\contracts"
RIGHT_COLUMN_WIDTH = 350
# IMAGE_DIR = os.path.join(__file__, "..", "images.sikuli")
IMAGE_DIR = os.path.join("C:/Workspaces/EOS/eoside/sikuli_movies/definitions.py", "..", "images.sikuli")
WAIT = True

X = 0
Y = 0
W = 854
H = 480

def wait(time_sec):
    if WAIT:
        time.sleep(time_sec)

def get_image(file_name):
    return os.path.join(IMAGE_DIR, "", file_name + ".png")

def get_region_vscode(window_title="EOS IDE - Visual Studio Code"):
    app = sikuli.App(window_title)
    print(app)
    sikuli.App.focus(window_title)
    return sikuli.App.focusedWindow()

#region_vscode = get_region_vscode()
region_vscode = sikuli.Region(X, Y, W, H)
X = region_vscode.getX()
Y = region_vscode.getY()
W = region_vscode.getW()
H = region_vscode.getH()

region_vscode.highlight
print(region_vscode)
focus_vscode = sikuli.Region(X+W-100, Y+50, 100, 100)
status_bar = sikuli.Region(X, Y+H-20, W, 20)
region_side_bar = sikuli.Region(X, Y+30, 240, H-50)
region_menu_bar = sikuli.Region(X, Y, W, 30)
region_file_selection = sikuli.Region(X, Y+30, W, 25)
region_column_border = sikuli.Region(X+W-RIGHT_COLUMN_WIDTH, Y+250, 0, 0)
region_right_column = sikuli.Region(
    X+W-RIGHT_COLUMN_WIDTH, X+50, RIGHT_COLUMN_WIDTH, H-50)


def open_folder(folder_name):
    region_vscode.find(get_image("open_folder/new_folder")).click()
    region_vscode.wait(get_image("new_folder_change_name"))
    wait(1)
    region_vscode.type(sikuli.Key.BACKSPACE )
    region_vscode.type(folder_name + "\n")
    region_vscode.wait(get_image("open_folder/open"))
    region_vscode.click(region_vscode.getLastMatch())


def open_file(path):
    if not os.path.isabs(path):
        path = os.path.join(CONTRACT_DIR, path)
    region_vscode.type(focus_vscode, "o", sikuli.Key.CTRL)
    region_vscode.wait(get_image("file_name"))
    region_vscode.type(get_image("file_name"), path)
    region_vscode.click(get_image("open_folder/open"))


def send_sortcut(letter, key_modifiers=sikuli.Key.CTRL):
    region_vscode.type(focus_vscode, letter, key_modifiers)

MODIFIERS = {
    "CTRL": sikuli.Key.CTRL,
    "ALT": sikuli.Key.ALT,
    "CND": sikuli.Key.CMD,
    "META": sikuli.Key.META,
    "SHIFT": sikuli.Key.SHIFT,
    "WIN": sikuli.Key.WIN,
    "ALTGR": sikuli.Key.ALTGR
    }

def send_k(letter, modifier=None):
    region_vscode.type(focus_vscode, "k", sikuli.Key.CTRL)
    if modifier:
        region_vscode.type(focus_vscode, letter, MODIFIERS[modifier])
    else:
        region_vscode.type(focus_vscode, letter)


def go_to_file(go_to_file_image_name):
    go_to_file_image = get_image(go_to_file_image_name)
    region_vscode.type(focus_vscode, "p", sikuli.Key.CTRL) 
    region_vscode.click(go_to_file_image)


def set_side_bar(on=True):
    if not region_vscode.exists(get_image("side_bar_is_on")) == on:
        region_vscode.type(focus_vscode, "b", sikuli.Key.CTRL) 

def toggle_panel():
    region_vscode.hover()
    region_vscode.type(focus_vscode, "j", sikuli.Key.CTRL)

def panel(on=True):
    terminal = region_vscode.exists(get_image("TERMINAL"))
    if on and not terminal or not on and terminal:
       toggle_panel()

# region_vscode.exists("C:/Workspaces/EOS/eoside/sikuli_movies/images.sikuli/explorer_is_on").getScore() 1; 0.75

# region_vscode.exists("C:/Workspaces/EOS/eoside/sikuli_movies/images.sikuli/side_bar_is_on").getScore() 0.98; 0.78; 0.82; 0.81; 0.94/


def narration(narration_text, action="a"):
    region_vscode.type(
        find("file_selection/narration", region_file_selection), 
            "s", sikuli.Key.CTRL)
    narration_file = file(NARRATION_FILE, action)
    print(narration_file)
    narration_file.write(narration_text)
    narration_file.close()

def narration_type(narration_text, action="a"):
    wait_image("file_selection/narration", region_file_selection)
    if action=="w":
            region_vscode.type(
                find("file_selection/narration", region_file_selection),
                "a", sikuli.Key.CTRL)
            region_vscode.type(
                find("file_selection/narration", region_file_selection),
                sikuli.Key.BACKSPACE)

    send_k("q", "CTRL")
    region_vscode.type(
        region_file_selection.find(get_image("file_selection/narration")),
        narration_text)


def find(image, region=region_vscode):
    return region.find(get_image(image))


def hover(image, region=region_vscode):
    return region.hover(get_image(image))


def exists(image, region=region_vscode):
    return region.exists(get_image(image))


def wait_image(image, region=region_vscode):
    return region.wait(get_image(image))


def click(image, region=region_vscode):
    return region.click(get_image(image))

def drag_drop(image, region, image_region=region_vscode):
    column_border = find(image, image_region)
    return column_border.dragDrop(column_border, region)
