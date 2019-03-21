import sys
import os
import shutil
import subprocess
import time
import org.sikuli.script as sikuli

VSCODE = "eosfactory - Visual Studio Code"
NARRATION_FILE = "C:\\Workspaces\\EOS\\eoside\\sikuli_movies\\narration.md"
CONTRACT_DIR = "C:\\Workspaces\\EOS\\contracts"
RIGHT_COLUMN_WIDTH = 350
IMAGE_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "images.sikuli")

FF_MPEG = "ffmpeg.exe"
MOVIES_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "movies")
MOVIES_FORMAT = "mp4" #"wmv"
MOVIES_FRAM_RATE = 8

WAIT = True
START_POINT = "start_point"

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
region_file_selection = sikuli.Region(X, Y+20, W, 35)
region_column_border = sikuli.Region(X+W-RIGHT_COLUMN_WIDTH, Y+250, 0, 0)
region_right_column = sikuli.Region(
    X+W-RIGHT_COLUMN_WIDTH, X+50, RIGHT_COLUMN_WIDTH, H-50)


def open_folder(folder_name):
    find("open_folder/new_folder").click()
    wait_image("new_folder_change_name")
    wait(1)
    region_vscode.type(sikuli.Key.BACKSPACE )
    region_vscode.type(folder_name + "\n")
    wait_image("open_folder/open").click()


def open_file(path):
    if not os.path.isabs(path):
        path = os.path.join(CONTRACT_DIR, path)
    region_vscode.type(focus_vscode, "o", sikuli.Key.CTRL)
    region_vscode.wait(get_image("file_name"))
    region_vscode.type(get_image("file_name"), path)
    region_vscode.click(get_image("open_folder/open"))


def send_shortcut(letter, key_modifiers=sikuli.Key.CTRL):
    region_vscode.type(focus_vscode, letter, key_modifiers)


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


def delete_contract(contract_dir):
    try:
        if os.path.exists(contract_dir):
            shutil.rmtree(contract_dir)
    except Exception as e:
        print(e)


def set_settings(contract_dir):
    with open (os.path.join(
            os.path.dirname(__file__), START_POINT, ".vscode\settings.json"),
                "r") as file:
        settings = file.read()
    with open(os.path.join(contract_dir, ".vscode\settings.json"), "w") as file:
        file.write(settings)


def focus_editor_title(name, group=1):
    region = region_menu_bar
    region.type(region, str(group), sikuli.Key.CTRL)
    region.type(region, "p", sikuli.Key.CTRL)
    region.type(region, name + "\n")


def focus_group(group):
    region = region_menu_bar
    region.type(region, str(group), sikuli.Key.CTRL)


class Edit():
    def __init__(self, name, group=1):
        self.name = name
        self.group = group

    def focus_group(self, group=None):
        if not group:
            group = self.group
        
        self.group = group
        region = region_menu_bar
        region.type(region, str(group), sikuli.Key.CTRL)

    def focus_editor(self, group=None):
        self.focus_group(group)
        region = region_menu_bar
        region.type(region, "p", sikuli.Key.CTRL)
        region.type(region, self.name + "\n")

    def type(self, text, action="a", end_of_file=True):
        self.focus_group()

        if action == "w":
            region_vscode.type("a", sikuli.Key.CTRL)
            region_vscode.type(sikuli.Key.BACKSPACE)

        if end_of_file:
            region_vscode.type(sikuli.Key.END, sikuli.Key.CTRL)
        else:
            region_vscode.type("k", sikuli.Key.CTRL)
            region_vscode.type("q", sikuli.Key.CTRL)

        region_vscode.type(text)


def toggle_side_bar():
    region_menu_bar.type(region_menu_bar, "b", sikuli.Key.CTRL)


def find(PSMRL, region=region_vscode):
    if isinstance(PSMRL, str):
        PSMRL = get_image(PSMRL)
    return region.find(PSMRL)


def hover(PSMRL, region=region_vscode):
    if isinstance(PSMRL, str):
        PSMRL = get_image(PSMRL)
    return region.hover(PSMRL)


def exists(PSMRL, region=region_vscode):
    if isinstance(PSMRL, str):
        PSMRL = get_image(PSMRL)
    return region.exists(PSMRL)


def wait_image(PSMRL, region=region_vscode):
    if isinstance(PSMRL, str):
        PSMRL = get_image(PSMRL)
    return region.wait(PSMRL)


def click(PSMRL, region=region_vscode):
    if isinstance(PSMRL, str):
        PSMRL = get_image(PSMRL)
    return region.click(PSMRL)      


def drag_drop(PSMRL, region, PSMRL_region=region_vscode):
    if isinstance(PSMRL, str):
        PSMRL = find(PSMRL, PSMRL_region)
    return PSMRL_region.dragDrop(PSMRL, region)     


def type(PSMRL, text, region=region_vscode, modifiers=None):
    if isinstance(PSMRL, str):
        PSMRL = find(get_image(PSMRL), PSMRL_region)
    if modifiers:
        region.type(PSMRL, text, sikuli.Key.CTRL)
    else:
        region.type(PSMRL, text)     


def save_all():
    send_k("s")


def escape(PSMRL=focus_vscode):
    if isinstance(PSMRL, str):
        PSMRL = get_image(PSMRL)
        
    type(PSMRL, sikuli.Key.ESC)


def kill_ffmpeg():
    subprocess.Popen(
        ['taskkill', "/IM", FF_MPEG],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    subprocess.Popen(
        ['taskkill', "/IM", FF_MPEG],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)



# start "Ffmpeg from sikuli" ffmpeg -f gdigrab -framerate 10 -offset_x 0 -offset_y 0 -video_size 854x480 -show_region 1 -i desktop C:\Workspaces\EOS\eoside\sikuli_movies\movies\test.wmv
def start_ffmpeg(output_file, 
        format=MOVIES_FORMAT, frame_rate=MOVIES_FRAM_RATE):

    if not os.path.isabs(output_file):
        output_file = os.path.join(MOVIES_DIR, output_file)

    output_file = output_file + "." + format

    try:
        if os.path.exists(output_file):
            os.remove(output_file)
    except:
        print("Cannot remove the file ()".format(output_file))

    video_size = "{}x{}".format(W, H)
    arg = [
        "cmd", "/c", "start", "/MIN",
        FF_MPEG, "-f", "gdigrab", "-framerate", str(frame_rate), "-offset_x", str(X), "-offset_y", str(Y), "-video_size", video_size, "-show_region", str(1), "-i", "desktop", output_file]

    print(" ".join(arg))
    subprocess.Popen(arg)

        

