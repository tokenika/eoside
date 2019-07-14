import sys
import os
import shutil
import subprocess
import time
import threading
import json
import inspect
import org.sikuli.basics as basics
import org.sikuli.script as sikuli
import sikuli_movies

SETUP = '''
# Setup

* eosio version 1.8.0
* eosio.cdt version 1.6.1
* EOSFactory version 3.4.0
* EOSIDE version 1.1.1
'''

def sikuli_movies_dir():
    return os.path.realpath(os.path.dirname(sikuli_movies.__file__))

CONTRACT_WORKSPACE = "C:\\Workspaces\\EOS\\contracts\\"
DOCS_STATIC = "C:\\Workspaces\\EOS\\eoside\\docs\\_static"
MOVIES_DIR = os.path.join(sikuli_movies_dir(), "movies")
RIGHT_COLUMN_WIDTH = 350
TERMINAL_HIGHT = 200
IMAGE_DIR = os.path.realpath(
    os.path.join(os.path.dirname(sikuli_movies.__file__), "images.sikuli"))
NARRATION_FILE = os.path.realpath(
    os.path.join(os.path.dirname(sikuli_movies.__file__), "movies", 
    "narration.md"))

FF_MPEG = "ffmpeg.exe"
MOVIES_FORMAT = "mp4" #"wmv"
MOVIES_FRAM_RATE = 25

X = 50
Y = 50
W = 854
H = 480

REGION_VSCODE = sikuli.Region(X, Y, W, H)
FOCUS_VSCODE = sikuli.Region(X + 700, Y, 20, 25)
REGION_SIDE_BAR = sikuli.Region(X, Y + 30, 240, H-50)
REGION_FILE_SELECTION_BAR = sikuli.Region(X, Y+25, W, 30)
REGION_TITLE_BAR = sikuli.Region(X, Y, W, 30)
REGION_COLUMN_BORDER = sikuli.Region(
                        X+W-RIGHT_COLUMN_WIDTH, Y + H - TERMINAL_HIGHT, 0, 0)
REGION_TERMINAL = sikuli.Region(X, Y + H - 150, W, 150)

# black, blue, cyan, gray, green, magenta, orange, pink, red, white, yellow
basics.Settings.DefaultHighlightColor = "PINK"
################################################################################
# Switch verbosity status:
basics.Settings.ActionLogs = False
def excepthook(type, value, traceback):
    print(value)
# sys.excepthook = excepthook
################################################################################


def wait(time_sec):
    time.sleep(time_sec)


def sleep(time_sec):
    wait(time_sec)


def get_image(file_name):
    path = os.path.join(IMAGE_DIR, file_name + ".png")
    if not os.path.exists(path):
        exit('''
The path 
'{}'
does not exist.
'''.format(path))

    return os.path.join(IMAGE_DIR, file_name + ".png")


# def get_region_vscode(window_title="EOSIDE - Visual Studio Code"):
#     app = sikuli.App(window_title)
#     print(app)
#     sikuli.App.focus(window_title)
#     return sikuli.App.focusedWindow()


def ACTION(msg=None, module_level=2):
    module_level = min(len(inspect.stack()) - 1, module_level)
    function_name = inspect.stack()[module_level - 1][3].replace("_", " ")

    if inspect.stack()[module_level][3] == "<module>":  
        print(">" * 50)
        title = ">>> " + function_name
        print(title if not msg else title + msg)

    return function_name


def CUT(module_level=2):
    module_level = min(len(inspect.stack()) - 1, module_level)
    if inspect.stack()[module_level][3] == "<module>":
        print("<" * 50 + "\n")


def set_special_effects(contract_dir, special_effects=[]):
    ACTION(": {}".format(special_effects))

    if not special_effects:
        special_effects = ["ignoreeoside,"]
    else:
        special_effects = ["ignoreeoside," + special_effects[0]]

    path = os.path.join(contract_dir, ".vscode\settings.json")
    with open (path, "r") as infile:
            settings = json.load(infile)
            settings["eoside.specialEffects"] = special_effects
            with open(os.path.join(
                contract_dir, ".vscode\settings.json"), "w") as outfile:
                json.dump(settings, outfile, indent=4)
    CUT()


def create_folder(
        folder_name,
        PS=None, region=REGION_VSCODE, seconds=3, wait=0, score=0):
    ACTION()

    find("open_folder/new_folder").click()
    wait_image("new_folder_change_name")
    sleep(1)
    REGION_VSCODE.type(sikuli.Key.BACKSPACE )
    REGION_VSCODE.type(folder_name + "\n")
    sleep(2)    
    wait_image("open_folder/open").click()
    detected = None
    if PS:
        detected = wait_image(PS, region, seconds, wait, score)

    CUT()
    return detected


def set_folder(path, open_image):
    folder = wait_image("open_folder/folder")
    REGION_VSCODE.type(FOCUS_VSCODE, path + "\n")
    wait(3)
    wait_image(open_image).click()


def open_file(
        path,
        PS=None, region=REGION_VSCODE, seconds=3, wait=0, score=0):
    ACTION()
    
    if not os.path.isabs(path):
        path = os.path.join(CONTRACT_WORKSPACE, path)
    print("The path is {}.".format(path))

    REGION_VSCODE.type(FOCUS_VSCODE, "o", sikuli.Key.CTRL)
    REGION_VSCODE.wait(get_image("file_name"))
    REGION_VSCODE.type(get_image("file_name"), path)
    REGION_VSCODE.click(get_image("open_folder/open"))

    detected = None
    if PS:
        detected = wait_image(PS, region, seconds, wait, score)
    CUT()
    return detected


def copy_recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                copy_recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)


def open_folder(
        path,
        PS=None, region=REGION_VSCODE, seconds=3, wait=0, score=0):
    ACTION()
    
    if not os.path.isabs(path):
        path = os.path.join(CONTRACT_WORKSPACE, path)
    print("The path is {}.".format(path))

    REGION_VSCODE.type(FOCUS_VSCODE, "ko", sikuli.Key.CTRL)
    folder = REGION_VSCODE.wait(get_image("open_folder/folder"))
    REGION_VSCODE.type(folder, path + "\n")
    REGION_VSCODE.click(get_image("open_folder/select_folder"))

    detected = None
    if PS:
        detected = wait_image(PS, region, seconds, wait, score)
    CUT()
    return detected



def new_file(path):
    FOCUS_VSCODE.type(FOCUS_VSCODE, "n", sikuli.Key.CTRL)
    FOCUS_VSCODE.type(FOCUS_VSCODE, "s", sikuli.Key.CTRL)
    FOCUS_VSCODE.type(FOCUS_VSCODE, path)
    REGION_VSCODE.find(get_image("open_folder/save")).click()


def send_shortcut(letter, key_modifiers=sikuli.Key.CTRL):
    FOCUS_VSCODE.type(FOCUS_VSCODE, letter, key_modifiers)
    return FOCUS_VSCODE


def send_k(letter, modifier=None):
    FOCUS_VSCODE.type(FOCUS_VSCODE, "k", sikuli.Key.CTRL)
    if modifier:
        FOCUS_VSCODE.type(FOCUS_VSCODE, letter, MODIFIERS[modifier])
    else:
        FOCUS_VSCODE.type(FOCUS_VSCODE, letter)


def go_to_file(go_to_file_image_name):
    go_to_file_image = get_image(go_to_file_image_name)
    FOCUS_VSCODE.type(FOCUS_VSCODE, "p", sikuli.Key.CTRL) 
    FOCUS_VSCODE.click(go_to_file_image)


# REGION_VSCODE.exists("C:/Workspaces/EOS/eoside/sikuli_movies/images.sikuli/explorer_is_on").getScore() 1; 0.75

# REGION_VSCODE.exists("C:/Workspaces/EOS/eoside/sikuli_movies/images.sikuli/side_bar_is_on").getScore() 0.98; 0.78; 0.82; 0.81; 0.94/


def delete_contract(contract_workspace, contract_name):

    for suffix in ["1"]:
        name = contract_name + suffix
        path = os.path.join(contract_workspace, name)
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
            return name
        except Exception as e:
            pass

    print('''
While trying to delete the file
    {},
the following error message is issued:
    {}
'''.format(path, str(e)))
    exit(str(e))


def set_settings(contract_dir, start_point):
    '''Copies workspace settings to the folder 'contract_dir`.
    '''
    ACTION()
    with open (os.path.join(start_point, ".vscode\settings.json"), 
            "r") as file:
        settings = file.read()

    with open(
        os.path.join(contract_dir, ".vscode\settings.json"), "w") as file:
        file.write(settings)
    CUT()


def set_c_cpp_properties(contract_dir, start_point):
    '''Copies workspace settings to the folder 'contract_dir`.
    '''
    ACTION()
    with open (os.path.join(start_point, ".vscode\c_cpp_properties.json"),
                                                                "r") as file:
        c_cpp_properties = file.read()
    with open(
            os.path.join(contract_dir, ".vscode\c_cpp_properties.json"), 
            "w") as file:
        file.write(c_cpp_properties)
    CUT()


def focus_group(group):
    FOCUS_VSCODE.type(FOCUS_VSCODE, str(group), sikuli.Key.CTRL)


def find(PSMRL, region=REGION_VSCODE, score=0):
    if isinstance(PSMRL, str):
        PSMRL = get_image(PSMRL)
    result = region.find(PSMRL)

    if result.getScore() >= score:
        return result


def hover(PSMRL, wait=0, region=None):
    if isinstance(PSMRL, str):
        if not region:
            region = find(PSMRL)
        could_be_moved = region.hover(get_image(PSMRL))
    else:
        if not region:
            region = REGION_VSCODE
        could_be_moved = region.hover(PSMRL)

    if wait:
        sleep(wait)
    
    return region


def exists(PSMRL, region=REGION_VSCODE, score=0):
    if isinstance(PSMRL, str):
        PSMRL = get_image(PSMRL)

    result = region.exists(PSMRL)
    if result and result.getScore() >= score:
        return result


def exit(msg):
    kill_ffmpeg()
    raise Exception("ERROR:" + msg)


def wait_image(PS, region=REGION_VSCODE, seconds=3, wait=0, score=0):

    PERIOD = 1
    count = seconds / PERIOD
    detected = None

    if isinstance(PS, str):
        PS = get_image(PS)

    while True:
        detected = region.exists(PS)
        if detected and detected.getScore() > score:
            print
            break
        else:
            print ".", 
            sys.stdout.flush()
            time.sleep(PERIOD)

        count = count - 1
        if count < 0:
            print
            exit('''
Waiting for {}, the waiting time {} exceeded.
            '''.format(str(PS), seconds))

    time.sleep(wait)
    return detected


def click(PSMRL, region=REGION_VSCODE):
    if isinstance(PSMRL, str):
        PSMRL = get_image(PSMRL)
    return region.click(PSMRL)      


def drag_drop(PSMRL, region, PSMRL_region=REGION_VSCODE):
    if isinstance(PSMRL, str):
        PSMRL = find(PSMRL, PSMRL_region)
    return PSMRL_region.dragDrop(PSMRL, region)     


def type(PSMRL, text, region=REGION_VSCODE, modifiers=None):
    if isinstance(PSMRL, str):
        PSMRL = find(get_image(PSMRL), PSMRL_region)
    if modifiers:
        region.type(PSMRL, text, sikuli.Key.CTRL)
    else:
        region.type(PSMRL, text)     


def save_all(wait_time=1.5):
    ACTION()
    send_k("s")
    wait(wait_time)
    CUT()


def escape(PSMRL=FOCUS_VSCODE):
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

def raw_name(output_file, video_format):
    return output_file + "_raw." + video_format


def start_ffmpeg(
                    movie_base_name, 
                    video_format=MOVIES_FORMAT, frame_rate=MOVIES_FRAM_RATE):

    output_file = raw_name(movie_base_name, video_format)

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


def make_linking_bat(movie_base_name, cwd, play=False, video_format=MOVIES_FORMAT):
    FADE_TIME = 1
    fade_n = int(round(FADE_TIME * MOVIES_FRAM_RATE))

    movie_raw_file = raw_name(movie_base_name, video_format)
    movie_faded_file = movie_base_name + "_faded." + video_format
    movie_file = os.path.join(
            DOCS_STATIC, os.path.basename(movie_base_name) + "." + video_format)

    script = '''
ffmpeg -y -i {0} -vf "fade=in:0:{1:d}" -c:v libx264 -crf 23  -pix_fmt yuv420p -movflags faststart {2}
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy {3}
    '''.format(
        movie_raw_file, fade_n, movie_faded_file, movie_file)

    if play:
        script = script + '''
ffplay {}
    '''.format(movie_file)

    with open(os.path.join(cwd, "link.bat"), "w+") as f:
        f.write(script)


def make_title_fading_bat(cwd, video_format=MOVIES_FORMAT):
    NAME = "title"
    TIME = 4
    FADE_TIME = 1

    fade_n = int(round(FADE_TIME * MOVIES_FRAM_RATE))
    fade_out_n = (TIME - FADE_TIME) * MOVIES_FRAM_RATE

    movie_faded_file = NAME + "_faded." + video_format

    script = '''
ffmpeg -y -loop 1 -i {0}.png -c:v libx264 -crf 23 -pix_fmt yuv420p -pix_fmt yuv420p -movflags faststart -t 4 -framerate {1:d} {0}.mp4
'''.format(NAME, MOVIES_FRAM_RATE, TIME)

    script = script + '''
ffmpeg -y -i {0}.mp4 -vf "fade=in:0:{1:d}, fade=out:{3:d}:{1:d}" -c:v libx264 -crf 23  -pix_fmt yuv420p -movflags faststart {2}
    '''.format(NAME, fade_n, movie_faded_file, fade_out_n)

    with open(os.path.join(cwd, "title_fading.bat"), "w+") as f:
        f.write(script)


def make_concat_parts_bat(movie_base_name, cwd, video_format=MOVIES_FORMAT):
    # https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg
    # ffmpeg -i opening.mkv -i episode.mkv -i ending.mkv -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" output.mkv

    # ffmpeg -i part1_raw.mp4 -i part2_raw.mp4 -filter_complex "[0:v] [1:v] concat=n=2:v=1 [v]" -map "[v]" native_debugger_raw.mp4

    movie_raw_file = raw_name(movie_base_name, video_format)

    script = '''
ffmpeg -i part1_raw.{0} -i part2_raw.{0} -filter_complex "[0:v] [1:v] concat=n=2:v=1 [v]" -map "[v]" {1}
    '''.format(video_format, movie_raw_file)

    with open(os.path.join(cwd, "concat_parts.bat"), "w+") as f:
        f.write(script)


def go_top():
    FOCUS_VSCODE.type(
            FOCUS_VSCODE, sikuli.Key.HOME, sikuli.Key.CTRL)


def go_bottom():
    FOCUS_VSCODE.type(
            FOCUS_VSCODE, sikuli.Key.END, sikuli.Key.CTRL)


def close_current_editor():
    REGION_VSCODE.type(sikuli.Key.F4, sikuli.Key.CTRL)
