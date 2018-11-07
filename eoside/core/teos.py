#!/usr/bin/python3

import os
import subprocess
import time
import re
import pathlib
import shutil
import pprint

import eosfactory.core.logger as logger
import eosfactory.core.utils as utils
import eosfactory.core.setup as setup
import eosfactory.core.config as config
import eosfactory.core.errors as errors


TEMPLATE_CONTRACTS_DIR = "templates/contracts"
TEMPLATE_NAME = "CONTRACT_NAME"
TEMPLATE_EOSIO_DIR = "@EOSIO_DIR@"
TEMPLATE_HOME = "@HOME@"
TEMPLATE_ROOT = "@ROOT@"


def abi_eoside(c_cpp_properties_path,
        contract_dir_hint=None, code_name=None, verbosity=None):
    '''Given a hint to a contract directory, produce ABI file.
    '''
    contract_dir = config.contract_dir(contract_dir_hint)
    source = config.contract_source_files(contract_dir)
    srcs = source[1]
    if not srcs:
        raise errors.Error('''
        "The source is empty. The assumed contract dir is   
        {}
        '''.format(contract_dir))
        return

    if not code_name:
        code_name = os.path.splitext(os.path.basename(srcs[0]))[0]
    target_dir = get_target_dir(source[0])
    target_path_abi = os.path.normpath(
                        os.path.join(target_dir, code_name  + ".abi"))

    for src in srcs:
        srcPath = src
        if os.path.splitext(src)[1].lower() == ".abi":
            logger.INFO('''
            NOTE:
            An ABI exists in the source directory. Cannot overwrite it:
            {}
            Just copying it to the target directory.
            '''.format(src), verbosity)
            shutil.move(
                srcPath, os.path.join(target_dir, 
                os.path.basename(srcPath)))
            return 

    extensions = [".c", ".cpp",".cxx", ".c++"]
    sourcePath = srcs[0]
    source_dir = os.path.dirname(srcs[0])

    if os.path.exists(c_cpp_properties_path):
        try:
            with open(path, "r") as input:
                text = input.read()
                c_cpp_properties = json.loads(input.read())
        except Exception as e:
            raise errors.Error(str(e))
    else:
        raise errors.Error('''
            The given path does not exist:
            ${}       
        '''.format(c_cpp_properties_path))

    command_line = [
        config.abigen_exe(),
        "-extra-arg=-c", "-extra-arg=--std=c++14", 
        "-extra-arg=--target=wasm32", "-extra-arg=-nostdinc", 
        "-extra-arg=-nostdinc++", "-extra-arg=-DABIGEN"
    ]

    includes = c_cpp_properties["configurations"][0]["includePath"]
    for include in includes:
        command_line.append("-extra-arg=-I" + include)

    command_line.extend(
        [
            "-extra-arg=-fparse-all-comments",
            "-destination-file=" + target_path_abi,
            "-context=" + source_dir,
            sourcePath,
            "--"
        ]
    )

    if setup.is_print_command_line:
        print("######## {}:".format(config.abigen_exe()))
        print(" ".join(command_line))

    process(command_line)

    logger.TRACE('''
    ABI file writen to file: {}
    '''.format(target_path_abi), verbosity)


def wast_eoside(
        contract_dir_hint, code_name=None, 
        compile_only=False, verbosity=None):
    '''Given a hint to a contract directory, produce WAST and WASM code.
    '''

    contract_dir = config.contract_dir(contract_dir_hint)
    source = config.contract_source_files(contract_dir)
    srcs = source[1]
    if not srcs:
        raise errors.Error('''
        "The source is empty. The assumed contract dir is  
        {}
        '''.format(contract_dir))
        return

    targetPathWast = None
    target_dir_path = get_target_dir(source[0])

    workdir = os.path.join(target_dir_path, "working_dir")
    if not os.path.exists(workdir):
        os.makedirs(workdir)

    workdir_build = os.path.join(workdir, "build")
    if not os.path.exists(workdir_build):
        os.mkdir(workdir_build)    

    objectFileList = []
    extensions = [".h", ".hpp", ".hxx", ".c", ".cpp",".cxx", ".c++"]
    if not code_name:
        code_name = os.path.splitext(os.path.basename(srcs[0]))[0]
    targetPathWast = os.path.join(
        target_dir_path, code_name + ".wast")
    target_path_wasm = os.path.join(
        target_dir_path, code_name + ".wasm")

    eosio_cpp = None
    try:
        eosio_cpp = config.eosio_cpp()
    except:
        pass

    if eosio_cpp:
        command_line = [
            config.eosio_cpp(),
            "-o",
            target_path_wasm
            ]
        for file in srcs:
            if not os.path.splitext(file)[1].lower() in extensions:
                continue
            command_line.append(file)

        try:
            process(command_line)
        except Exception as e:                       
            raise errors.Error(str(e))
    else:
        ###########################################################################
        # eosio.cdt is not available.
        for file in srcs:
            if not os.path.splitext(file)[1].lower() in extensions:
                continue

            command_line = [
                config.wasm_clang_exe(),
                "-emit-llvm", "-O3", "--std=c++14", "--target=wasm32", "-nostdinc",
                "-nostdlib", "-nostdlibinc", "-ffreestanding", "-nostdlib",
                "-fno-threadsafe-statics", "-fno-rtti", "-fno-exceptions",
                "-I", config.eosio_repository_dir() 
                    + "/contracts/libc++/upstream/include",
                "-I", config.eosio_repository_dir() 
                    + "/contracts/musl/upstream/include",
                "-I", config.eosio_repository_dir() 
                    + "/externals/magic_get/include",
                "-I", config.boost_include_dir(),
                "-I", config.eosio_repository_dir() + "/contracts",
                "-I", config.eosio_repository_dir() + "/build/contracts",
                "-I", contract_dir
            ]

            if include_dir:
                include_dirs = include_dir.split(",")
                for dir in include_dirs:
                    command_line.extend(["-I", dir])

            output = os.path.join(workdir_build, code_name + ".o")
            objectFileList.append(output)        
            command_line.extend(["-c", file, "-o", output])
            
            if setup.is_print_command_line:
                print("######## {}:".format(config.wasm_clang_exe()))
                print(" ".join(command_line))

            try:
                process(command_line)
            except Exception as e:
                try:
                    shutil.rmtree(workdir)
                except:
                    pass
                            
                raise errors.Error(str(e))

        if not compile_only:
            command_line = [ 
                config.wasm_llvm_link_exe(),
                "-only-needed", 
                "-o",  workdir + "/linked.bc",
                " ".join(objectFileList),
                config.eosio_repository_dir() + "/build/contracts/musl/libc.bc",
                config.eosio_repository_dir() + "/build/contracts/libc++/libc++.bc",
                config.eosio_repository_dir() + "/build/contracts/eosiolib/eosiolib.bc"
            ]
            if setup.is_print_command_line:
                print("######## {}:".format(config.wasm_llvm_link_exe()))
                print(" ".join(command_line))

            try:
                process(command_line)
            except Exception as e:                           
                raise errors.Error(str(e))

            command_line = [
                config.wasm_llc_exe(),
                "-thread-model=single", "--asm-verbose=false",
                "-o", workdir + "/assembly.s",
                workdir + "/linked.bc"
            ]
            if setup.is_print_command_line:
                print("######## {}:".format(config.wasm_llc_exe()))
                print(" ".join(command_line))

            try:
                process(command_line)
            except Exception as e:
                raise errors.Error(str(e))
                try:
                    shutil.rmtree(workdir)
                except:
                    pass
                            
                raise errors.Error(str(e))          

            command_line = [
                config.s2wasm_exe(),
                "-o", targetPathWast,
                "-s", "16384",
                workdir + "/assembly.s"
            ]
            if setup.is_print_command_line:
                print("######## {}:".format(config.s2wasm_exe()))
                print(" ".join(command_line))

            try:
                process(command_line)
            except Exception as e:
                try:
                    shutil.rmtree(workdir)
                except:
                    pass
                            
                raise errors.Error(str(e))

            logger.TRACE('''
            WAST file writen to file: {}
            '''.format(os.path.normpath(targetPathWast)), verbosity)                      

            command_line = [
                config.wast2wasm_exe(), 
                targetPathWast, target_path_wasm, "-n"]

            if setup.is_print_command_line:
                print("######## {}:".format(config.wast2wasm_exe()))
                print(" ".join(command_line))

            try:
                process(command_line)
            except Exception as e:
                try:
                    shutil.rmtree(workdir)
                except:
                    pass
                            
                raise errors.Error(str(e))
        try:
            shutil.rmtree(workdir)
        except:
            pass

    logger.TRACE('''
    WASM file writen to file: {}
    '''.format(os.path.normpath(target_path_wasm)), verbosity)
