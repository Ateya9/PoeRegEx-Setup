import os
import re


output_path = os.fspath("./output/")
input_file_path = os.fspath("./input.txt")
log_file_path = os.fspath(output_path + "/log.txt")


def check_requirements() -> bool:
    """
    Checks whether the required file exists, and creates the output folder.
    :return:
    """
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    return os.path.exists(input_file_path)


def parse_list() -> None:
    if not check_requirements():
        print('Input file does not exist. Please paste the mods into a file called "input.txt".')
        return
    with open(log_file_path, "a") as log_file:
        with open(input_file_path, "r") as input_file:
            input_file_lines = input_file.readlines()
        mod_group = []
        for line in input_file_lines:
            if "increased Quantity of Items found in this Area" in line:
                continue
            elif "increased Rarity of Items found in this Area" in line:
                continue
            elif line.startswith(("map", "Prefix", "Suffix")):
                # Ignore irrelevant lines like 'map extra content weighting [0]'
                continue
            elif "increased Pack size" in line:
                # TODO: code to insert the data into the modgroup file
                mod_group = []
                continue
            output_line = line
            output_line = remove_preceding_mod_info(output_line)
            if output_line.startswith("Total"):
                # There should be one line with just 'Total', ignore this line.
                continue
            print(output_line)


def generate_mod_group_name(mod_group: list) -> str:
    pass


def remove_preceding_mod_info(string_to_process: str) -> str:
    """
    Removes the preceding mod information from the input string, such as weightings and mod types.
    :param string_to_process:
    :return:
    """
    output = string_to_process
    mod_types = ["physical_damage",
                 "elemental_damage",
                 "resource",
                 "life",
                 "physical",
                 "damage",
                 "elemental",
                 "fire",
                 "cold",
                 "lightning",
                 "chaos",
                 "attack",
                 "caster",
                 "speed",
                 "curse",
                 "ailment",
                 "bleed",
                 "poison",
                 "critical",
                 "defences",
                 "resistance"]
    while re.match("^[0-9].*$", output):
        # Remove all numbers at the start of the line.
        output = output[1:]
    i = 0
    while i < len(mod_types):
        if output.startswith(mod_types[i]):
            output = output.replace(mod_types[i], "", 1)
            # print(output)
            i = 0
        else:
            i += 1
    while re.match("^[0-9].*$", output):
        # Remove numbers that appear just after the mod types.
        output = output[1:]
    return output


if __name__ == "__main__":
    parse_list()
