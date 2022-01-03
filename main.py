import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Tool for read only unsecure lines with context')
parser.add_argument("-f", "--file", help="file, that will be proceseed")
parser.add_argument("-e", "--epsilon", help="allowed difference between inputed line and current", default=2)
parser.add_argument("-l", "--lines",
                    help="centers of context, format:\n"
                         "integers between dots, no spacebars, example:"
                         "3,7,12,13,14,25 ")
args = parser.parse_args()


def fatal_error(message: str):
    print(message)
    exit()


def read_file_as_list_of_lines(path_to_file: Path) -> list[str]:
    """ file can be very big, so, this operation can not be repeated """
    try:
        with open(path_to_file, "r") as fi:
            return fi.readlines()
    except FileNotFoundError:
        fatal_error(f"unreachable path {path_to_file} - file not found, return empty list")
    except UnicodeDecodeError as ude:
        fatal_error(f"{path_to_file} - unicode error: {ude}")


def acceptable_values(whole_file: list[str], input_pointers: list[int]) -> bool:
    if args.epsilon is not int or args.epsilon < 0:
        fatal_error("epsilon must be positive int")
    file_size = len(whole_file)
    for number in input_pointers:
        if number is not int or number < 1:
            fatal_error(f"wrong value: {number}")
        if number > file_size:
            print(f"W: have a pointer to {number}th line, but file have only {file_size} lines")
            input_pointers.remove(number)
    return bool(file_size > 0)


try:
    pointers: list[int] = args.lines.split(",")
    lines_to_filter = read_file_as_list_of_lines(args.file)
    if not acceptable_values(lines_to_filter, pointers):
        exit()


except Exception as e:
    print(f"undebugged error {e=}")

exit()
