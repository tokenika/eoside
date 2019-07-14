import os
import org.sikuli.script as sikuli
import sikuli_movies.core.definitions as de
import sikuli_movies.core.elements as el

REGION_CTRL_P_SELECTION = sikuli.Region(de.X+150, de.Y+50, de.W-150-300, 30)

def init(start_point, group=1):
    de.ACTION()
    if not sikuli.Region(de.X, de.Y, 30, 30).exists(de.get_image(
                                                        "assorted/vsc_icon")):
        de.exit("The VSCode window is not in position")
    de.kill_ffmpeg()
    el.ok_keyboard()
    el.hide_terminal_panel()
    
    if not de.exists("title_bar/start_point", de.REGION_TITLE_BAR):
        de.save_all()
        de.open_folder(start_point, "assorted/vsc_icon")

    el.hide_terminal_panel()
    el.hide_side_bar()
    el.close_all_editors()    
    
    narration = Edit("narration", group)
    if not narration.focus():
        de.open_file(de.NARRATION_FILE, "file_selection/narration")

    narration.type("", "w")
    print("Returning narration editor in group {}.".format(group))
    de.CUT()
    return narration


def init_part(start_point, contract_name, group=1):
    de.ACTION()
    if not sikuli.Region(de.X, de.Y, 30, 30).exists(de.get_image(
                                                        "assorted/vsc_icon")):
        de.exit("The VSCode window is not in position")
    de.kill_ffmpeg()
    el.ok_keyboard()
    el.hide_terminal_panel()

    de.save_all()
    de.copy_recursive_overwrite(
                start_point, os.path.join(de.CONTRACT_WORKSPACE, contract_name))

    el.hide_terminal_panel()
    el.hide_side_bar()
    el.close_all_editors()
    
    narration = Edit("narration", 1)
    if not narration.focus():
        de.open_file(de.NARRATION_FILE, "file_selection/narration")

    narration.type("", "w")
    print("Returning narration editor in group {}.".format(group))
    de.CUT()
    return narration


'''
reload(de)
reload(el)
reload(st)
narration = st.Edit("narration", 1)

'''

class SikuliObject():
    def __init__(self, name, group=1):
        de.ACTION()
        print("{} in group {}".format(name, group))
        self.name = name
        self.group = self.limits(group)
        de.focus_group(group)
        de.CUT()

    def limits(self, group):
        if group <=1:
            return 1
        if group >= 2:
            return 2

    def go_top(self):
        de.ACTION(" <= " + self.name)
        self.focus()
        de.FOCUS_VSCODE.type(de.FOCUS_VSCODE, sikuli.Key.HOME, sikuli.Key.CTRL)
        de.sleep(0.5)
        de.CUT()

    def go_bottom(self):
        de.ACTION(" <= " + self.name)
        self.focus()
        de.FOCUS_VSCODE.type(de.FOCUS_VSCODE, sikuli.Key.END, sikuli.Key.CTRL)
        de.sleep(0.5)
        de.CUT()

    def go_to_line(self, line):
        de.ACTION(" <= " + self.name)
        self.focus()
        de.FOCUS_VSCODE.type(de.FOCUS_VSCODE, "g", sikuli.Key.CTRL)
        de.FOCUS_VSCODE.type(de.FOCUS_VSCODE, str(line) + "\n")
        de.sleep(0.5)
        de.CUT() 

    def scroll_down(self, count):
        de.ACTION(" <= " + self.name)
        if count:
            self.focus()
            for i in range(0, count):
                de.FOCUS_VSCODE.type(
                            de.FOCUS_VSCODE, sikuli.Key.DOWN, sikuli.Key.CTRL)
                de.sleep(0.5)
        de.CUT()

    def focus_group(self, group=None):
        de.ACTION(" <= " + self.name)
        if not group:
            group = self.group
        
        self.group = self.limits(group)
        de.FOCUS_VSCODE.type(de.FOCUS_VSCODE, str(self.group), sikuli.Key.CTRL)
        de.CUT()

    def focus(self, group=None):
        de.ACTION(" <= " + self.name)
        self.focus_group(group)
        result = True

        if not de.exists("title_bar/{}".format(self.name)):
            region = de.FOCUS_VSCODE
            region.type(region, "p", sikuli.Key.CTRL)
            region.type(region, self.name + "\n")
            if de.exists("assorted/no_results_found", REGION_CTRL_P_SELECTION):
                print "No results found!"
                result = False
        de.CUT()
        return result

    def move_right(self):
        de.ACTION(" <= " + self.name)
        region = de.FOCUS_VSCODE
        self.focus()
        de.FOCUS_VSCODE.type(sikuli.Key.RIGHT, sikuli.Key.CTRL + sikuli.Key.ALT)
        self.group = 2
        de.wait(0.5)
        de.CUT()
        
    def move_left(self):
        de.ACTION(" <= " + self.name)
        self.focus()
        de.FOCUS_VSCODE.type(sikuli.Key.LEFT, sikuli.Key.CTRL + sikuli.Key.ALT)
        self.group = 1
        de.wait(0.5)
        de.CUT()


class View(SikuliObject):
    def focus(self, group=None):
        de.ACTION(" <= " + self.name)
        self.focus_group(group)
        result = True

        if not de.exists("title_bar/{}".format
                                        (self.name.replace("EOSIDE:", ""))):
            region = de.FOCUS_VSCODE
            region.type(region, "p", sikuli.Key.CTRL)
            region.type(region, ">" + self.name + "\n")
            result = True
            if de.exists("assorted/no_commands_found", REGION_CTRL_P_SELECTION):
                print "No commands found!"
                result = False
        de.CUT()
        return result


class EOSIDEview(View):
    def __init__(
                    self, PS=None, region=de.REGION_VSCODE, 
                    seconds=3, wait=0, score=0, group=1):
        SikuliObject.__init__(self, "EOSIDE:EOSIDE", group)
        de.ACTION(self.name)
        self.detected = el.show_shortcut_view(
                                            "eoside/installed",
                                            "e",
                                            sikuli.Key.CTRL + sikuli.Key.ALT,
                                            "Show EOSIDE get started view",
                                            PS, region, seconds, wait, score)
        de.CUT()


class SetupView(View):
    def __init__(
                    self, PS=None, region=de.REGION_VSCODE, 
                    seconds=3, wait=0, score=0, group=1):
        SikuliObject.__init__(self, "EOSIDE:Setup", group)
        de.ACTION(self.name)
        self.detected = el.show_shortcut_view(
                                            "setup/installed", 
                                            "s",
                                            sikuli.Key.CTRL + sikuli.Key.ALT,
                                            "Show EOSIDE setup view",
                                            PS, region, seconds, wait, score)
        de.CUT()


class InstallView(View):
    def __init__(
                    self, PS=None, region=de.REGION_VSCODE, 
                    seconds=3, wait=0, score=0, group=1):
        SikuliObject.__init__(self, "EOSIDE:Install", group)
        de.ACTION(self.name)
        self.detected = el.show_shortcut_view(
                                            "install/installed",
                                            "i",
                                            sikuli.Key.CTRL + sikuli.Key.ALT,
                                            "Show EOSIDE install view",
                                            PS, region, seconds, wait, score)
        de.CUT()
        

class Edit(SikuliObject):
    def __init__(self, name, group=1):
        de.ACTION("Edit")
        SikuliObject.__init__(self, name, group)
        de.CUT()

    def type(self, text, action="a", end_of_file=True):
        if action == "w":
            msg = "write"
        else:
            if end_of_file:
                msg = "append"
            else:
                msg = "continue"
        de.ACTION(" {} in group {}".format(self.name, self.group))
        print(text.decode('utf-8','ignore').encode("utf-8"))

        self.focus()
        if action == "w":
            de.REGION_VSCODE.type("a", sikuli.Key.CTRL)
            de.REGION_VSCODE.type(sikuli.Key.BACKSPACE)

        if end_of_file:
            de.REGION_VSCODE.type(sikuli.Key.END, sikuli.Key.CTRL)
        else:
            de.REGION_VSCODE.type("k", sikuli.Key.CTRL)
            de.REGION_VSCODE.type("q", sikuli.Key.CTRL)

        de.REGION_VSCODE.type(text)
        de.CUT()        

    def set_width(self):
        de.ACTION()
        ## Move column border
        de.drag_drop(
            de.find("column_border1").offset(3, 0), de.REGION_COLUMN_BORDER)
        de.CUT()

class Terminal():
    def __init__(self):
        de.ACTION("Terminal")
        de.CUT()

    def is_shown(self):
        return de.exists("terminal/TERMINAL", de.REGION_VSCODE)

    def set_hight(self):
        de.ACTION(" <= Terminal")
        top_border = de.exists("terminal/TERMINAL")
        if top_border:
            de.drag_drop(top_border.offset(0, -15), de.REGION_COLUMN_BORDER)
        de.CUT()

    def show(self):
        de.ACTION(" <= Terminal")
        if not self.is_shown():
            el.show_terminal()
        de.CUT()

    def hide(self):
        de.ACTION(" <= Terminal")
        el.hide_terminal_panel()
        de.CUT()

    def new(self, maximize=False):
        de.ACTION(" <= Terminal")
        el.new_bash_terminal()
        if not maximize:
            self.set_hight()
        else:
            self.maximize()
        de.CUT()

    def type(self, text, new_line=True):
        de.ACTION(" <= Terminal")
        self.show()
        if new_line:
            text = text + "\n"
        de.REGION_VSCODE.type(de.get_image("terminal/TERMINAL"), text)
        de.FOCUS_VSCODE.hover()
        de.CUT()

    def maximize(self):
        de.ACTION(" <= Terminal")
        if not self.is_shown():
            return
        button = de.REGION_VSCODE.exists(de.get_image("terminal/maximize"))
        if button and button.getScore() >= 0.85:
            button.click()
            de.REGION_VSCODE.type(
                    de.get_image("terminal/TERMINAL"), 
                    sikuli.Key.HOME, sikuli.Key.CTRL)
        de.CUT()
        
    def minimize(self):
        de.ACTION(" <= Terminal")
        if not self.is_shown():
            return
        button = de.REGION_VSCODE.exists(de.get_image("terminal/minimize"))
        if button and button.getScore() >= 0.95:
            button.click()
            de.REGION_VSCODE.type(
                                de.get_image("terminal/TERMINAL"), 
                                sikuli.Key.HOME, sikuli.Key.CTRL)
        de.CUT()

    def scroll_down(self, count):
        de.ACTION(" <= Terminal")
        de.REGION_VSCODE.type(sikuli.Key.HOME, sikuli.Key.CTRL)
        for i in range(0, count):
            de.REGION_VSCODE.type(sikuli.Key.DOWN, sikuli.Key.CTRL)
            de.sleep(0.5)
        de.CUT()
          

def build_contract():
    de.ACTION()
    de.FOCUS_VSCODE.type(
                    de.FOCUS_VSCODE, "b", sikuli.Key.CTRL + sikuli.Key.SHIFT)
    print("Waiting for terminal/eosio-cpp_OK1")
    de.wait_image("terminal/eosio-cpp_OK1", seconds=20, score=0.85)
    de.CUT()


def compile_contract():
    de.ACTION()
    de.FOCUS_VSCODE.type(de.FOCUS_VSCODE, "c", sikuli.Key.CTRL + sikuli.Key.SHIFT)
    print("Waiting for terminal/eosio-cpp_OK1")
    de.wait_image("terminal/eosio-cpp_OK1", seconds=20, score=0.85)    
    de.CUT()


def make_contract(arguments="", clear=True):
    de.ACTION()

    terminal = Terminal()
    terminal.new(maximize=True)
    terminal.type(" cd build")
    de.wait(1)
    if clear:
        terminal.type(" rm -r *")
        de.wait(1)
    
    terminal.type(" cmake {} ..".format(arguments))
    de.wait(2)
    terminal.type(" make")
    print("Waiting for terminal/eosio-cpp_OK1")
    de.wait_image("terminal/eosio-cpp_OK1", de.REGION_TERMINAL, seconds=20, score=0.85)

    de.CUT()
    return terminal


def run_test(test_name, scroll_count):
    de.ACTION()
    
    terminal = Terminal()
    terminal.new(maximize=True)
    terminal.type(" python3 tests/{}".format(test_name))
    de.wait_image("terminal/local_node_stopped2", seconds=25, score=0.85)

    de.wait(2)
    terminal.scroll_down(scroll_count)

    de.CUT()
    return terminal


def show_file(file_name, dir_name, scroll_count=0):
    de.ACTION()

    el.show_explorer()
    de.focus_group(1) 
    if not de.exists(
            "explorer/{}".format(file_name), de.REGION_SIDE_BAR, score=0.85):
        de.find("explorer/{}".format(dir_name), de.REGION_SIDE_BAR).click()
        de.hover(de.FOCUS_VSCODE)
    
    de.wait_image(
        "explorer/{}".format(file_name), de.REGION_SIDE_BAR, score=0.85).click()

    el.hide_side_bar()
    editor = Edit(file_name, 1)
    if scroll_count:
        editor.go_top()
        editor.scroll_down(count=scroll_count)

    de.CUT()
    return editor


def show_and_run_test(test_name, scroll_script_count, scroll_result_count):
    de.ACTION()
    show_file(test_name, "tests", scroll_script_count)
    terminal = run_test(test_name, scroll_result_count)
    de.CUT()
    return terminal


def new_text_file(path, group=1):
    de.ACTION()
    region = de.FOCUS_VSCODE
    region.type(region, "n", sikuli.Key.CTRL)
    region.type(region, "s", sikuli.Key.CTRL)
    region.type(region, path)
    de.REGION_VSCODE.find(de.get_image("open_folder/save")).click()
    file_name = os.path.basename(path)
    editor = Edit(file_name, group)
    de.CUT()
    return editor