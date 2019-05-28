## ["&"warning: GDB: Failed to set controlling terminal "](https://github.com/Microsoft/vscode-cpptools/issues/264)


[And there:](https://developercommunity.visualstudio.com/content/problem/206839/warning-gdb-failed-to-set-controlling-terminal-ope.html)
The message "warning: GDB: Failed to set controlling terminal" is actually a long standing bug in gdb when the debuggee's output is redirected to a tty and is harmless.

[The message comes from GDB when it is being passed --tty command line in order to redirect the stdin/out.

We have intercepted and suppressed the message in VS 15.8, but the warning is still there anyway.

The warning message is harmless, is it not a blocking issue at all.