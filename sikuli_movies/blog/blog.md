## [Lacley](https://github.com/glitchassassin/lackey)

Lackey is a Python implementation of Sikuli script, allowing you to run automation scripts developed in the Sikuli editor with pure Python. If you're trying to run Sikuli scripts in a Java-free environment or integrate them into an existing Python testing structure, this is the library for you.


## SikuliX with jython

Environment variable: `CLASSPATH: C:\\SikuliX\\sikulixapi.jar`

```python
>>> import sys
>>> sys.path.append("C:\\SikuliX\\sikulixapi.jar")
>>> from org.sikuli.script.SikulixForJython import *
```

Better, copy `C:\\SikuliX\\sikulixapi.jar` to `C:\jython2.7.0\javalib`. Then

```python
import org.sikuli.script as sikuli
REGION_VSCODE = sikuli.Region(0,0,854,480)
print(REGION_VSCODE)
```

## Interactive mode

Set `%SIKULI_HOME%` as `c:\SikuliX`

```
java -jar %SIKULI_HOME%\sikulix.jar -i
>>> capture()
u'C:\\Users\\cartman\\AppData\\Local\\Temp\\Sikulix_1924393810\\sikuliximage-1559127225135.png'
>>>
```

## How to capture context menus --- use capture hotkey

There is a so called "Capture Hot Key", that can be used in these cases:

- have Sikuli IDE started
- prepare the GUI situation where you want to capture something
- press the hotkey
- the capture mode should come up
- the captured image is inserted at the IDE's cursor position

look menu File -> Preferences for the current definition (standard is CTRL-SHIFT-2)