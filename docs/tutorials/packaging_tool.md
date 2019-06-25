# Packaging tool

If you want to pass to a colleague your EOSIO contract project which is a VSCode folder, the fist guess, is to zip the folder and e-mail it. However, this plan is not quite straightforward:

* There are volume binaries there.
* There are local configuring files in the `.vscode` folder.
* There are your private notes and scratchpads there.
* The paths in the `.vscode/c_cpp_properties.json` are localized according to your operating system.

Hence, you should copy the folder, and edit it.

EOSIDE implements EOSFactory tool [`eosfactory.pack_contract.py`](https://eosfactory.io/build/html/tutorials/ExchangingContractProject.html) that helps to organize the distribution process:

* The `Zip` button in the `Setup` view or (ctrl/cmd+alt+z) calls the EOSFactory command `eosfactory.pack_contract.py`: it zips the current (processed) project. The result goes to the root of the project.
* The `Open zip file` in the `EOSIDE` view does the opposite: it restores a project from a zip file. If the zip results from the packaging process, it is readjusted to the current conditions.


