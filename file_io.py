def read_protected_file(path_to_file:str) -> tuple[bool, str]:
    """
    Returns a protected file that needs sudo permissions to be read
    :param path_to_file: path to the file to be read
    :return:
        [True, content of the file] if the reading succeeds, else
        [False, error text]
    """
    try:
        with open(path_to_file, "r") as f:
            content = f.read()
        return True, content
    except PermissionError:
        return False, "Not enough permissions. Did you add sudo before running the code ?"
    except FileNotFoundError:
        return False, "File " + path_to_file + " does not exist."
    except Exception:
        return False, "Unknown error reading the file: " + path_to_file

def write_protected_file(path_to_file:str, content:str) -> tuple[bool, str]:
    """
    Writes to a protected file that needs sudo permission to be written
    :param path_to_file: path to the file to be written
    :param content: The content to be written with
    :return:
        [True, ""] if the writing succeeds, else
        [False, error text]
    """
    try:
        with open(path_to_file, "w") as f:
            f.write(content)
        return True, ""
    except PermissionError:
        return False, "Not enough permissions. Did you add sudo before running the code ?"
    except Exception:
        return False, "Unknown error writing the file: " + path_to_file