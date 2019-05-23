import sys
import os
import shutil
import subprocess
import time
import json
import org.sikuli.script as sikuli
import sikuli_movies

VSCODE = "eosfactory - Visual Studio Code"
NARRATION_FILE = "C:\\Workspaces\\EOS\\eoside\\sikuli_movies\\narration.md"
CONTRACT_DIR = "C:\\Workspaces\\EOS\\contracts"
RIGHT_COLUMN_WIDTH = 350
TERMINAL_HIGHT = 200
IMAGE_DIR = os.path.realpath(
    os.path.join(os.path.dirname(sikuli_movies.__file__), "images.sikuli"))

FF_MPEG = "ffmpeg.exe"
MOVIES_FORMAT = "mp4" #"wmv"
MOVIES_FRAM_RATE = 25

WAIT = True

X = 0
Y = 0
W = 854
H = 480

def sikuli_movies_dir():
    return os.path.realpath(os.path.dirname(sikuli_movies.__file__))

def wait(time_sec):
    if WAIT:
        time.sleep(time_sec)

def get_image(file_name):
    return os.path.join(IMAGE_DIR, file_name + ".png")

def get_region_vscode(window_title="EOSIDE - Visual Studio Code"):
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

print(region_vscode)
focus_vscode = sikuli.Region(X + W - 100, Y + 50, 100, 100)
status_bar = sikuli.Region(X, Y+H-20, W, 20)
region_side_bar = sikuli.Region(X, Y + 30, 240, H-50)
region_menu_bar = sikuli.Region(X + 700, Y, 20, 25)
region_file_selection = sikuli.Region(X, Y+20, W, 35)
region_column_border = sikuli.Region(
    X+W-RIGHT_COLUMN_WIDTH, Y + H - TERMINAL_HIGHT, 0, 0)
region_right_column = sikuli.Region(
    X+W-RIGHT_COLUMN_WIDTH, X+50, RIGHT_COLUMN_WIDTH, H-50)
region_terminal = sikuli.Region(
    X, Y + H - TERMINAL_HIGHT, W, TERMINAL_HIGHT)
region_scroll = sikuli.Region(X + W - 20, Y + H - 27, 20, 27)


def build():
    focus_vscode.type(focus_vscode, "b",
                                        sikuli.Key.CTRL + sikuli.Key.SHIFT)


def compile():
    focus_vscode.type(focus_vscode, "c",
                                        sikuli.Key.CTRL + sikuli.Key.SHIFT)


def show_enabled_extensions():
    region_menu_bar.type(region_menu_bar, "x", 
                                        sikuli.Key.CTRL + sikuli.Key.SHIFT)
    region_menu_bar.type(region_menu_bar, "e", 
                                        sikuli.Key.CTRL)


def set_special_effects(contract_dir, special_effects=[]):
    with open (os.path.join(
        contract_dir, ".vscode\settings.json"), "r") as infile:
            settings = json.load(infile)
            settings["eoside.specialEffects"] = special_effects
            with open(os.path.join(
                contract_dir, ".vscode\settings.json"), "w") as outfile:
                json.dump(settings, outfile, indent=4)


def open_folder(folder_name):
    find("open_folder/new_folder").click()
    wait_image("new_folder_change_name")
    wait(1)
    region_vscode.type(sikuli.Key.BACKSPACE )
    region_vscode.type(folder_name + "\n")
    wait_image("open_folder/open").click()


def set_folder(path):
    folder = wait_image("open_folder/folder")
    region_vscode.type(region_menu_bar, path + "\n")
    wait_image("open_folder/open").click()


def open_file(path):
    if not os.path.isabs(path):
        path = os.path.join(CONTRACT_DIR, path)
    region_vscode.type(focus_vscode, "o", sikuli.Key.CTRL)
    region_vscode.wait(get_image("file_name"))
    region_vscode.type(get_image("file_name"), path)
    region_vscode.click(get_image("open_folder/open"))


def new_file(path):
    region_menu_bar.type(region_menu_bar, "n", sikuli.Key.CTRL)
    region_menu_bar.type(region_menu_bar, "s", sikuli.Key.CTRL)
    region_menu_bar.type(
        region_menu_bar, path)
    region_vscode.find(get_image("open_folder/save")).click()


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
        msg = '''
While trying to delete the file
    {},
the follwing error message is issued:
    {}
'''.format(contract_dir, str(e))
        print(msg)
        exit()


def set_settings(contract_dir, start_point):
    '''Copies workspace settings to the folder 'contract_dir`.
    '''
    with open (os.path.join(
            os.path.dirname(__file__), start_point, ".vscode\settings.json"),
                "r") as file:
        settings = file.read()
    with open(os.path.join(contract_dir, ".vscode\settings.json"), "w") as file:
        file.write(settings)

    with open (os.path.join(
                            os.path.dirname(__file__), start_point, 
                            ".vscode\c_cpp_properties.json"),
                                                                "r") as file:
        c_cpp_properties = file.read()
    with open(
                            os.path.join(contract_dir, 
                            ".vscode\c_cpp_properties.json"), "w") as file:
        file.write(c_cpp_properties)


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
        self.group = self.limits(group)

    def limits(self, group):
        if group <=1:
            return 1
        if group >= 2:
            return 2

    def scroll_down(self, count):
        self.focus_editor()
        region_vscode.type(sikuli.Key.HOME, sikuli.Key.CTRL)
        for i in range(0, count):
            region_vscode.type(sikuli.Key.DOWN, sikuli.Key.CTRL)
            time.sleep(0.5)

    def focus_group(self, group=None):
        if not group:
            group = self.group
        
        self.group = self.limits(group)
        region = region_menu_bar
        region.type(region, str(self.group), sikuli.Key.CTRL)

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

    def move_right(self):
        region = region_menu_bar
        region.type(region, "1", sikuli.Key.CTRL)
        region.type(region, "p", sikuli.Key.CTRL)
        region.type(region, self.name + "\n")
        region.type(sikuli.Key.RIGHT, sikuli.Key.CTRL + sikuli.Key.ALT)
        self.group = 2

    def move_left(self):
        region = region_menu_bar
        region.type(region, "2", sikuli.Key.CTRL)
        region.type(region, "p", sikuli.Key.CTRL)
        region.type(region, self.name + "\n")
        region.type(sikuli.Key.LEFT, sikuli.Key.CTRL + sikuli.Key.ALT)
        self.group = 1

    def set_width(self):
        ## Move column border
        drag_drop(
            find("column_border").offset(5, 0), region_column_border)


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


def wait_image(PS, region=region_vscode, seconds=3, wait=0, score=0):
    if isinstance(PS, str):
        PS = get_image(PS)
    count = 2 * seconds
    exists = None
    while True:
        exists = region.exists(PS)
        if exists and exists.getScore() > score:
            break
        else:
            time.sleep(0.5)
        count = count - 1
        if count < 0:
            break
    if wait:
        time.sleep(wait)
    return exists


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


def save_all(wait_time=1.5):
    send_k("s")
    wait(wait_time)


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

'''
https://superuser.com/questions/859010/what-ffmpeg-command-line-produces-video-more-compatible-across-all-devices

ffmpeg \
    -f gdigrab -framerate 25 -offset_x 0 -offset_y 0 -video_size 854x480 -show_region 1 \
    -i desktop \
    -c:v libx264 -crf 23 -pix_fmt yuv420p \
    -movflags faststart \
    output.mp4
'''

def raw_name(output_file, format):
    return output_file + "_raw." + format


def start_ffmpeg(output_file, 
        format=MOVIES_FORMAT, frame_rate=MOVIES_FRAM_RATE):

    if not os.path.isabs(output_file):
        output_file = os.path.join(output_file)

    output_file = raw_name(output_file, format)

    try:
        if os.path.exists(output_file):
            os.remove(output_file)
    except:
        print("Cannot remove the file ()".format(output_file))

    video_size = "{}x{}".format(W, H)
    arg = [
        "cmd", "/c", "start", "/MIN",
        FF_MPEG, "-f", "gdigrab", "-framerate", str(frame_rate), 
        "-offset_x", str(X), "-offset_y", str(Y), "-video_size", video_size, "-show_region", str(1), 
        "-i", "desktop", 
        "-c:v", "libx264", "-crf", str(23), "-pix_fmt", "yuv420p", 
        output_file]

    print(" ".join(arg))
    subprocess.Popen(arg)


def make_linking_bat(output_file, format=MOVIES_FORMAT):
    fade_time = 1
    fade_n = int(round(fade_time * MOVIES_FRAM_RATE))
    script = '''
ffmpeg -y -i {0} -vf "fade=in:0:{3:d}" -c:v libx264 -crf 23  -pix_fmt yuv420p -movflags faststart {2}_faded.{1}
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy ../../../docs/_static/{2}.{1}
    '''.format(
        raw_name(output_file, format), format, output_file, fade_n)

    with open("link.bat", "w+") as f:
        f.write(script)


class Terminal():
    def is_shown(self):
        return exists("terminal/TERMINAL", region_vscode)

    def set_hight(self):
        top_border = exists("terminal/TERMINAL")
        if top_border:
            drag_drop(top_border.offset(0, -15), region_column_border)

    def show(self):
        if not self.is_shown():
            # region_menu_bar.type(
            #     region_menu_bar, "b", sikuli.Key.CTRL + sikuli.Key.ALT)
            # find("terminal/TERMINAL").click()
            region_menu_bar.type(region_menu_bar, "j", sikuli.Key.CTRL)

    def hide(self):
        if self.is_shown():
            region_menu_bar.type(region_menu_bar, "j", sikuli.Key.CTRL)

    def new(self):
        region_menu_bar.type(
            region_menu_bar, "b", sikuli.Key.CTRL + sikuli.Key.ALT)
        self.set_hight()

    def type(self, text, new_line=True):
        self.show()
        if new_line:
            text = text + "\n"
        region_vscode.type(
            get_image("terminal/TERMINAL"), text)

    def maximize(self):
        if not self.is_shown():
            return
        button = region_vscode.exists(get_image("terminal/maximize"))
        if button:
            button.click()
            region_vscode.type(
                    get_image("terminal/TERMINAL"), 
                    sikuli.Key.HOME, sikuli.Key.CTRL)
        
    def minimize(self):
        if not self.is_shown():
            return
        button = region_vscode.exists(get_image("terminal/minimize"))
        if button:
            button.click()
            region_vscode.type(
                                get_image("terminal/TERMINAL"), 
                                sikuli.Key.HOME, sikuli.Key.CTRL)        

    def scroll_down(self, count):
        region_vscode.type(sikuli.Key.HOME, sikuli.Key.CTRL)
        for i in range(0, count):
            region_vscode.type(sikuli.Key.DOWN, sikuli.Key.CTRL)
            time.sleep(0.5)
          

def go_top():
    region_menu_bar.type(
            region_menu_bar, sikuli.Key.HOME, sikuli.Key.CTRL)


def go_bottom():
    region_menu_bar.type(
            region_menu_bar, sikuli.Key.END, sikuli.Key.CTRL)


def close_current_editor():
    region_vscode.type(sikuli.Key.F4, sikuli.Key.CTRL)
