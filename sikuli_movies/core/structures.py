import org.sikuli.script as sikuli
import sikuli_movies.core.definitions as de
import sikuli_movies.core.elements as el

def init(group=1):
    de.ACTION()
    if not sikuli.Region(de.X, de.Y, 30, 30).exists(de.get_image(
                                                        "assorted/vsc_icon")):
        de.exit("The VSCode window is not in position")
    el.ok_keyboard()
    de.kill_ffmpeg()

    el.hide_terminal_panel()    
    el.hide_side_bar()
    el.close_all_editors()
    de.open_file(de.NARRATION_FILE, "file_selection/narration")
    print("Returning narration editor in group {}.".format(group))
    de.CUT()
    return Edit("narration", group)


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
        de.CUT()

    def limits(self, group):
        if group <=1:
            return 1
        if group >= 2:
            return 2

    def go_top(self):
        de.ACTION()
        self.focus()
        de.REGION_VSCODE.type(sikuli.Key.HOME, sikuli.Key.CTRL)
        de.CUT()

    def go_bottom(self):
        de.ACTION()
        self.focus()
        de.REGION_VSCODE.type(sikuli.Key.END, sikuli.Key.CTRL)
        de.CUT()        

    def scroll_down(self, count):
        de.ACTION()
        self.focus()
        de.REGION_VSCODE.type(sikuli.Key.HOME, sikuli.Key.CTRL)
        for i in range(0, count):
            de.REGION_VSCODE.type(sikuli.Key.DOWN, sikuli.Key.CTRL)
            de.sleep(0.5)
        de.CUT()

    def focus_group(self, group=None):
        de.ACTION()
        if not group:
            group = self.group
        
        self.group = self.limits(group)
        region = de.FOCUS_VSCODE
        region.type(region, str(self.group), sikuli.Key.CTRL)
        de.CUT()

    def focus(self, group=None):
        de.ACTION()
        self.focus_group(group)
        region = de.FOCUS_VSCODE
        region.type(region, "p", sikuli.Key.CTRL)
        region.type(region, self.name + "\n")
        de.CUT()

    def move_right(self):
        de.ACTION()
        region = de.FOCUS_VSCODE
        region.type(region, "1", sikuli.Key.CTRL)
        region.type(region, "p", sikuli.Key.CTRL)
        region.type(region, self.name + "\n")
        region.type(sikuli.Key.RIGHT, sikuli.Key.CTRL + sikuli.Key.ALT)
        self.group = 2
        de.wait(0.5)
        de.CUT()
        
    def move_left(self):
        de.ACTION()
        region = de.FOCUS_VSCODE
        region.type(region, "2", sikuli.Key.CTRL)
        region.type(region, "p", sikuli.Key.CTRL)
        region.type(region, self.name + "\n")
        region.type(sikuli.Key.LEFT, sikuli.Key.CTRL + sikuli.Key.ALT)
        self.group = 1
        de.CUT()


class EOSIDEview(SikuliObject):
    def __init__(
                    self, PS=None, region=de.REGION_VSCODE, 
                    seconds=3, wait=0, score=0, group=1):
        SikuliObject.__init__(self, "EOSIDE", group)
        de.ACTION(self.name)
        self.detected = el.show_shortcut_view(
                                            "eoside/installed",
                                            "e",
                                            sikuli.Key.CTRL + sikuli.Key.ALT,
                                            "Show EOSIDE get started view",
                                            PS, region, seconds, wait, score,
                                            module_level=2)
        de.CUT()


class View(SikuliObject):
    def focus(self, group=None):
        de.ACTION()
        self.focus_group(group)
        region = de.FOCUS_VSCODE
        region.type(region, "p", sikuli.Key.CTRL)
        region.type(region, ">" + self.name + "\n")
        de.CUT()    


class SetupView(View):
    def __init__(
                    self, PS=None, region=de.REGION_VSCODE, 
                    seconds=3, wait=0, score=0, group=1):
        SikuliObject.__init__(self, "Setup", group)
        de.ACTION(self.name)
        self.detected = el.show_shortcut_view(
                                            "setup/installed", 
                                            "s",
                                            sikuli.Key.CTRL + sikuli.Key.ALT,
                                            "Show EOSIDE setup view",
                                            PS, region, seconds, wait, score,
                                            module_level=2)
        de.CUT()


class InstallView(View):
    def __init__(
                    self, PS=None, region=de.REGION_VSCODE, 
                    seconds=3, wait=0, score=0, group=1):
        SikuliObject.__init__(self, "Install", group)
        de.ACTION(self.name)
        self.detected = el.show_shortcut_view(
                                            "install/installed",
                                            "i",
                                            sikuli.Key.CTRL + sikuli.Key.ALT,
                                            "Show EOSIDE install view",
                                            PS, region, seconds, wait, score,
                                            module_level=2)
        de.CUT()
        

class Edit(View):
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
        print(text)

        self.focus_group()
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
        de.ACTION()
        top_border = de.exists("terminal/TERMINAL")
        if top_border:
            de.drag_drop(top_border.offset(0, -15), de.REGION_COLUMN_BORDER)
        de.CUT()

    def show(self):
        de.ACTION()
        el.show_terminal()
        de.CUT()

    def hide(self):
        de.ACTION()
        el.hide_terminal_panel()
        de.CUT()

    def new(self):
        de.ACTION()
        el.new_bash_terminal()
        self.set_hight()
        de.CUT()

    def type(self, text, new_line=True):
        de.ACTION()
        self.show()
        if new_line:
            text = text + "\n"
        de.REGION_VSCODE.type(
            de.get_image("terminal/TERMINAL"), text)
        de.CUT()

    def maximize(self):
        de.ACTION()
        if not self.is_shown():
            return
        button = de.REGION_VSCODE.exists(de.get_image("terminal/maximize"))
        if button:
            button.click()
            de.REGION_VSCODE.type(
                    de.get_image("terminal/TERMINAL"), 
                    sikuli.Key.HOME, sikuli.Key.CTRL)
        de.CUT()
        
    def minimize(self):
        de.ACTION()
        if not self.is_shown():
            return
        button = de.REGION_VSCODE.exists(de.get_image("terminal/minimize"))
        if button:
            button.click()
            de.REGION_VSCODE.type(
                                de.get_image("terminal/TERMINAL"), 
                                sikuli.Key.HOME, sikuli.Key.CTRL)
        de.CUT()

    def scroll_down(self, count):
        de.ACTION()
        de.REGION_VSCODE.type(sikuli.Key.HOME, sikuli.Key.CTRL)
        for i in range(0, count):
            de.REGION_VSCODE.type(sikuli.Key.DOWN, sikuli.Key.CTRL)
            de.sleep(0.5)
        de.CUT()
          

def build_contract():
    de.ACTION()
    de.FOCUS_VSCODE.type(
                    de.FOCUS_VSCODE, "b", sikuli.Key.CTRL + sikuli.Key.SHIFT)
    print("Waiting for terminal/eosio-cpp_OK")
    de.wait_image("terminal/eosio-cpp_OK", seconds=20, score=0.95)
    de.CUT()


def compile_contract():
    de.ACTION()
    de.FOCUS_VSCODE.type(de.FOCUS_VSCODE, "c", sikuli.Key.CTRL + sikuli.Key.SHIFT)
    print("Waiting for terminal/eosio-cpp_OK")
    de.wait_image("terminal/eosio-cpp_OK", seconds=20, score=0.95)    
    de.CUT()


def make_contract():
    de.ACTION()

    terminal = Terminal()
    terminal.new()
    terminal.type("cd build")
    de.wait(1)
    terminal.type("cmake ..")
    de.wait(1)
    terminal.type("make")
    print("Waiting for terminal/eosio-cpp_OK")
    de.wait_image("terminal/eosio-cpp_OK", seconds=20, score=0.95)

    de.CUT()
    return terminal


def run_test(test_name, scroll_count):
    de.ACTION()
    
    terminal = Terminal()
    terminal.new()
    terminal.maximize()    
    terminal.type("cd tests")
    terminal.type("python3 {}".format(test_name))
    de.wait_image("terminal/local_node_stopped", seconds=20, score=0.9)

    de.wait(2)
    terminal.scroll_down(scroll_count)

    de.CUT()
    return terminal


def show_file(file_name, dir_name, scroll_count):
    de.ACTION()

    el.show_explorer()
    de.focus_group(1) 
    if not de.exists("explorer/{}".format(file_name), de.REGION_SIDE_BAR):
        # expand the folder src:
        de.find("explorer/{}".format(dir_name), de.REGION_SIDE_BAR).click()
        de.hover(de.FOCUS_VSCODE) # move cursor away
    de.wait_image("explorer/hello.cpp", de.REGION_SIDE_BAR).click()

    de.wait_image("explorer/{}".format(file_name), de.REGION_SIDE_BAR).click()
    el.hide_side_bar()
    editor = Edit(file_name, 1)
    editor.scroll_down(count=scroll_count)

    de.CUT()
    return editor


def show_and_run_test(test_name, scroll_script_count, scroll_result_count):
    de.ACTION()
    show_file(test_name, "tests", scroll_script_count)
    terminal = run_test(test_name, scroll_result_count)
    de.CUT()
    return terminal

