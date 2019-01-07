# *EOSIde* -- Integrated Development Environment for EOSIO smart contracts

 With [*EOSIO*](https://github.com/eosio) installed in the System, *EOSIde* organizes the workflow of development process for EOSIO smart contracts -- if such a process can be seen as composed of the following elements:

* project standardization and bookkeeping,
* referencing documentation and tutorials,
* automatic availability of standard libraries,
* dependency management,
* compilation and build,
* debugging and testing,
* deployment.

*EOSIde* bases on [Visual Studio Code](https://code.visualstudio.com/), extending specifically functionalities of the *VSCode*.

## Preview of the application

User interface of EOSIde is composed of two views: one is displayed -- with the default configuration -- if VSCode is started empty: `code -n ""`. Let us list the functions of this view, shown in the picture below.

![Get Started view](docs/images/get_started.png)

* *Get Started* entries link to tutorials and other documentation.
* *New project* entries trigger creation of template projects.
* *Recent* entries switch to projects started with the *New project* triggers.
* *Open* entries trigger specific actions.
* Two menu buttons in the editor title bar, namely `|EOS IDE|` and `|Setup|` display corresponding views.


Another view is about the setup of the current EOSIO smart contract project. It is shown in the picture below.

![Setup view](docs/images/setup.png)

* *Include* lists directories contain headers involved in the project. This list copies the corresponding one in the `.vscode/c_cpp_properties.json` file that comes from *ms-vscode.cpptools*. The entries are provided with buttons that can manipulate them, especially, new items can be added with a system-native file dialog. With *Windows* and WSL Ubuntu, all file paths are expressed relative to the `WSL root`.
* *Libs* lists libraries resolving outer dependencies of the project.
* *Compiler Options* lists parameters of the wasm compiler.
* The buttons in the top, labelled *Compile*, *Build*, *EOS IDE* and *bash*, trigger corresponding actions. Especially, the *bash* button -- present if *Windows* -- starts a new *bash* terminal. All this actions can be invoked with keyboard shortcuts or with extension commands.

## Installation

EOSIde needs [*EOSIO*](https://github.com/eosio) to be installed in the system. Also, it needs *python3* (Ubuntu Python, even if the system is Windows with WSL Ubuntu).

![Setup view](docs/images/install.png)

