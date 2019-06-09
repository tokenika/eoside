import argparse
import os
import shutil
import org.sikuli.script as jsikuli
from org.sikuli.basics import HotkeyListener
from org.sikuli.basics import HotkeyManager
from org.sikuli.script import Env as JEnv


FORMAT = ".png"

class Env(JEnv):
    '''Copied from Lib\sikuli\Env.py in sikulixapi.jar
    '''

    @classmethod
    def addHotkey(cls, key, modifiers, handler):
        class AnonyListener(HotkeyListener):
            def hotkeyPressed(self, event):
                handler(event)
        return HotkeyManager.getInstance().addHotkey(
                                            key, modifiers, AnonyListener())

def main():
    '''Capture the image of a selected screen region.

    usage: sikuli_movies.core.capture [-h] [--wait] name
    
    positional arguments:
    name        Name of the image, absolute or relative to the 'images.sikuli'
                folder

    optional arguments:
    -h, --help  show this help message and exit
    --wait      Wait for a hotkey printed in a message on the start.
    '''

    parser = argparse.ArgumentParser(description='''
    Capture the image of a selected screen region.
    ''')
    parser.add_argument(
        "name", 
        help="Name of the image, absolute or relative to the 'images.sikuli' folder")
    parser.add_argument(
        "--wait", help="Wait for a hotkey printed in a message on the start.",
        action="store_true")
    args = parser.parse_args()

    def capture(event=None):
        try:
            shot = jsikuli.Screen(0).cmdCapture()
            image_file = args.name + FORMAT
            if not os.path.isabs(image_file):
                image_file = os.path.join(definitions.IMAGE_DIR, image_file)    
            shutil.copyfile(shot.getFile(), image_file)
            os.remove(shot.getFile())
        except:
            print "Capture aborted."
        exit()
    
    import definitions
    if args.wait:
        Env.addHotkey(
            "2", jsikuli.KeyModifier.SHIFT + jsikuli.KeyModifier.CTRL, capture)
    else:
        capture()


if __name__ == '__main__':
    main()