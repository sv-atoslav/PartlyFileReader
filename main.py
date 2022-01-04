import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description='Tool for read only unsecure lines with context')
parser.add_argument(
    "-f", "--file", type=Path, required=True,
    help="file, that will be processed")
parser.add_argument(
    # https://en.wikipedia.org/wiki/Epsilon_(disambiguation)#Mathematics
    "-e", "--epsilon", type=int, required=True,
    help="allowed difference between inputted line and current", default=2)
parser.add_argument(
    "-l", "--lines", required=True,
    help="centers of context, format:\n"
         "integers between dots, no spacebars, example:"
         "3,7,12,13,14,25 ")
args = parser.parse_args()


def fatal_error(message: str):
    print(message)
    exit()


# this action can not be repeat by business logic, so, i decide insert it directly at main function
# def read_file_as_list_of_lines(path_to_file: Path) -> list[str]:
#     try:
#         with open(path_to_file, "r") as fi:
#             return fi.readlines()
#     except FileNotFoundError:
#         fatal_error(f"unreachable path {path_to_file} - file not found, return empty list")
#     except UnicodeDecodeError as ude:
#         fatal_error(f"{path_to_file} - unicode error: {ude}")


# use usual dict instead
# class CodeCoordinate(NamedTuple):
#     number_of_line: int
#     content_of_line: str
#
#     def __gt__(self, other):
#         return self.number_of_line > other.number_of_line
#
#     def __lt__(self, other):
#         return self.number_of_line < other.number_of_line


# noinspection PyUnboundLocalVariable
def acceptable_values(input_pointers: list[int]) -> list[str]:
    """ return content of file, if all values are correct, else stop execution of program """
    if args.epsilon < 0:
        fatal_error("epsilon must be positive int")
    try:
        path_to_file = args.file
        with open(path_to_file, "r") as fi:
            unsorted_lines = fi.readlines()
    except FileNotFoundError:
        fatal_error(f"unreachable path {path_to_file} - file not found, return empty list")
    except UnicodeDecodeError as ude:
        fatal_error(f"{path_to_file} - unicode error: {ude}")
    file_size = len(unsorted_lines)
    for not_shadow_number in input_pointers:  # PyShadowingNames
        if not isinstance(not_shadow_number, int) or not_shadow_number < 1:
            fatal_error(f"wrong value: {not_shadow_number}")
        if not_shadow_number > file_size:
            print(f"W: have a pointer to {not_shadow_number}th line, but file have only {file_size} lines")
            input_pointers.remove(not_shadow_number)
    return unsorted_lines


def draw_file(lines: list[str], pointers: list[int], dispersion: int) -> list[dict]:
    """ used for show only lines, that "neighbours" to code with errors
    :param dispersion: "radius" for pieces, that will be exported
    :param pointers: list of "centers" of pieces
    :param lines: collection of strings, that already was read from file
    """
    whole_file = [""] + lines  # used for human-friendly pointers
    lines_to_show = []
    for index in range(1, len(whole_file)):
        for target in pointers:
            if abs(target - index) <= dispersion:
                lines_to_show.append({
                    'number_of_line': index,
                    'content_of_line': whole_file[index]})
                break  # if line (N) already append, skip and check line (N+1)
    return lines_to_show


input_pointers: list[int] = []
for number in args.lines.split(","):
    input_pointers.append(int(number))
filtered_values = draw_file(
    acceptable_values(input_pointers),
    input_pointers,
    args.epsilon)
with open(str("partly_" + Path(args.file).name + ".json"), 'w') as json_file:
    json.dump(filtered_values, json_file, indent=2, sort_keys=True)

exit()
