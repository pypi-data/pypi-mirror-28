import os
import subprocess
import sys
import logging
import coloredlogs

def check_already_exist(input_path):
    """
    Check if file already exists or not to avoid overwritting it

    Parameters
    ----------
    input_path : str
        Path to the file that is going to be checked

    Returns
    -------
    None

    """
    # TODO: Change this to a list of files
    if not isinstance(input_path, str):
        raise TypeError("Argument given to check format must be a string, it was " + str(type(input_path)))
    input_path = os.path.abspath(input_path)
    if os.path.exists(input_path):
        raise Exception('File "' + input_path + '" already exists, cannot overwrite it')


def run_cmd(cmd, output=0):
    """
    Function that runs a command given by user
    """

    if output == 0:
        process = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = process.stdout.readline()
        out = out.decode("utf-8").strip('\n')

        while out != '':
            print(out)
            out = process.stdout.readline()
            out = out.decode("utf-8").strip('\n')

    if output == 1:
        process = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = []
        out = process.stdout.readline()
        out = out.decode("utf-8").strip('\n')

        while out != '':
            output.append(out)
            out = process.stdout.readline()
            out = out.decode("utf-8").strip('\n')

        return output

    else :
        try:
            os.system(cmd)
        except :
            raise Exception("Command failed: " + cmd + "\n")


def check_format(file_list, suffix):
    """
    Check if all the files in a list passed by arguments fill the requirement
    of a specified suffix.

    Parameters
    ----------
    file_list : list
        List of paths (str) containing all files to check its format
    suffix : str
        String that contains the suffix that all files passed in the previous
        argument must have
    """

    # Check if input file_list is indeed a list of strings
    if not isinstance(file_list, list):
        raise TypeError("Argument given to check format must be a list of string")

    # Check if list if empty. In that case, raise exception
    check_empty(file_list)

    # Check if suffix is string
    if not isinstance(suffix, tuple):
        raise TypeError("Suffix must be a tuple (tuples of 1 must be \"(str,)\", don't forget the semicolon), it was " + str(type(suffix)))

    # For each file, see if file is a string and if suffix is the one that must be
    for file_name in file_list:
        if not isinstance(file_name, str):
            raise TypeError("Argument given to check format must be a string, it was " + str(type(file_name)))

        if file_name.endswith(suffix):
            return(None)
        else:
            raise NameError("Suffix of the file must be in " + str(suffix))


def setLogger(mode, module):
    """Define the log that we will use."""

    # create logger with 'spam_application'
    logger = logging.getLogger(module)
    logger.setLevel(logging.DEBUG)

    log = logging.StreamHandler()

    # Select the mode
    if mode is 'Debug':
        log.setLevel(level=logging.DEBUG)
    elif mode is 'Production':
        log.setLevel(level=logging.INFO)

    formatter = logging.Formatter('#[%(levelname)s] - %(name)s - %(message)s')
    log.setFormatter(formatter)

    # logger.addHandler(log)

    # read database here
    logger.info("Entering " + mode + " mode")

    return logger
