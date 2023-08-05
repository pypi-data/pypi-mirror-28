# find_tools.py

import os

def findfile(extension):
    """
    Returns name of file with extension in current working directory

    Args:
        extension: Examples include ".txt", ".pcr", ".py" etc.

    Raises:
        No exception is raised for multiple files with file ending "extension".
        but comments are printed to the console about the nature of extension
        and how many additional files were found.

    """
    files = [f for f in os.listdir() if f.endswith(extension)]
    searched_file = files[0] if len(files)==1 else "error!"
    if searched_file == "error!":
        print("error in folder:", os.getcwd())
        print("number of files with extension", "\"" + extension + "\"", "is", len(files))
    #     import pdb; pdb.set_trace()
    # else:
    return searched_file

def findfiles(extension):
    """
    Returns all files with specified extension in the current working directory

    Args:
        extension: Examples include ".txt", ".pcr", ".py" etc.

    Returns:
        list of files with specified extension.

    """
    return [f for f in os.listdir() if f.endswith(extension)]

def findfolders():
    """
    Returns all folders in current working directory

    Returns:
        list of directories in current working directory

    """
    return [f for f in os.listdir() if os.path.isdir(f)]
