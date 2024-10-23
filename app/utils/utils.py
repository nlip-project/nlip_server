import os
from pathlib import Path


# Various convenience routines to manipulate file names
def get_resolved_path(file_path: str) -> str:
    return str(Path(file_path).resolve().absolute())


def get_parent_location(file_path: str) -> str:
    parent = Path(file_path).parent
    return str(parent.resolve().absolute())


def get_joined_path(file_path_1: str, file_path_2: str) -> str:
    base_path = Path(file_path_1)
    this_path = base_path.joinpath(file_path_2)
    return str(this_path.resolve().absolute())


def make_destination_path(this_path: str) -> None:
    path = Path(this_path).resolve().absolute()
    path.parent.mkdir(parents=True, exist_ok=True)


def check_file_exists(filename):
    path = Path(filename).resolve().absolute()
    return os.path.exists(path)


def get_file_extension(filename: str):
    if "." in filename:
        return "." + filename.rsplit(".", 1)[-1]
    return None


"""
read a text file as a list
"""


def read_list(file_path: str):
    with open(file_path, "r") as file:
        lines = []
        for line in file:
            line = line.strip()
            if len(line) > 0:
                lines.append(line)
    return lines


def save_to_file(file_name: str, this_object: str):
    with open(file_name, "w") as text_file:
        text_file.write(this_object)


def read_from_file(file_name: str) -> str:
    with open(file_name, "r") as text_file:
        return text_file.read()


def mycompare(arg1: str, arg2: str) -> bool:
    if arg1 is not None and arg2 is not None:
        return arg1.lower().rstrip().lstrip() == arg2.lower().rstrip().lstrip()


def safe_index(this_char, input_string):
    if this_char in input_string:
        return input_string.index(this_char)
    else:
        return -1


"""
string_in_between extracts the first occurrence of lc, 
and the right-most occurrence of rc, and returns text between them. 
Both the characters are included in addition to the string

"""


def string_in_between(input_text: str, lc: chr, rc: chr) -> str:
    if lc in input_text and rc in input_text:
        lindex = input_text.index(lc)
        rindex = input_text.rindex(rc)
        return input_text[lindex : rindex + 1]
    elif lc in input_text:
        lindex = input_text.index(lc)
        return input_text[lindex:]
    elif rc in input_text:
        rindex = input_text.rindex(rc)
        return input_text[: rindex + 1]
    else:
        # Neither of the two characters occur
        return ""


"""
Checks whether char1 occurs before char2 in the input_text
returns True if char1 occurs before char2 
returns False if char2 occurs before cha1 
raises ValueError if one of char1 or char2 does not occur in the string
"""


def occurs_before(input_text: str, char1: chr, char2: chr):
    index_1 = input_text.index(char1)
    index_2 = input_text.rindex(char2)
    return index_1 < index_2


def get_class_name(this_object: object):
    return this_object.__class__.__name__


trace_flag = False


def trace_on():
    global trace_flag
    trace_flag = True


def trace_off():
    global trace_flag
    trace_flag = False


def trace_calls(func):
    global trace_flag

    def new_func(*args, **kwargs):
        if trace_flag:
            print(f"called {func.__name__} ({args} {kwargs})")
        response = func(*args, **kwargs)
        if trace_flag:
            print(f"call to {func.__name__} returned {response}")
        return response

    return new_func
