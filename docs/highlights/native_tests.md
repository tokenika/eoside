# Native unitest compilation and execution

## Setup options

There are two columns in the *Options* section in the *Setup* view. This view can be displayed with (ctrl/cmd+shift+p, then *eoside: |setup|*) or (ctrl/cmd+alt+s) or by clicking the *|Setup|* button in the editor title menu.

### Code Options

The left column sets options used for compilation and building of the contract code. 
Code compilation can be invoked with the button *Compile*, or with (ctrl/cmd+shift+p, then *eoside: compile*) or (ctrl/cmd+shift+c)

Code compilation and building can be invoked with the button *Build*, or with (ctrl/cmd+shift+p, then *eoside: build*) or (ctrl/cmd+shift+b)

### Test Options

The right column sets options used for compilation and building-execution of a native test. 
Here, compilation can be invoked with the button *Compile Test*, or with (ctrl/cmd+shift, then *eoside: compile test*) or (ctrl/cmd+alt+c)

Building-execution can be invoked with the button *Build and Run Test*, or with (ctrl/cmd+shift, then *eoside: build test*) or (ctrl/cmd+alt+b)

The values of options have to be taken from the list given by the command `eosio-cpp -help`, and from the following list:

* --src \<list of source file paths, absolute or relative to the project directory\> - A list of sources, if not set, they are found automatically.
* --verbose - If set, print the command line.


## Working example

Download to the system default download folder, this [zip file](https://github.com/tokenika/eosfactory.io/raw/master/examples/hello_with_native_test.zip). 
Alternatively, go [there](https://github.com/tokenika/eosfactory.io/blob/master/examples/hello_with_native_test.zip), right-click the *Download* button and set a download folder.

Next, switch to the *EOSIDE* view and use `Open: Open zip file` feature. As a result, you should have a working example of the EOSIO hello contract with a unitest.