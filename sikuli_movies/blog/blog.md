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
region_vscode = sikuli.Region(0,0,854,480)
print(region_vscode)
```

Ten limit jest wskazany w podstawowych dokumentach Pythona, dlatego uważam, że nie ma swobody wyboru, gdy już wybierzesz latający cyrk Pythona. 

