import os
import re
from slugify import slugify


output_folder = os.fspath("./output/")
log_file_path = os.fspath(output_folder + "/log.txt")


def check_requirements(required_file: str) -> bool:
    """
    Checks whether the required file exists, and creates the output folder.
    :return:
    """
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    return os.path.exists(required_file)


def parse_poedb_list(list_file_name: str) -> None:
    """
    Takes a file containing a raw copy+paste from poedb.tw, removes any extra info (such as mod weightings
    and types) and inserts the mod info into separate files in ./output.
    :param list_file_name:
    :return:
    """
    if not check_requirements(list_file_name):
        print('Input file does not exist. Please paste the mods into a file called "input.txt".')
        return
    with open(list_file_name, "r") as input_file:
        input_file_lines = input_file.readlines()
    mod_group = []
    for line in input_file_lines:
        output_line = line.strip()
        if "increased Quantity of Items found in this Area" in output_line:
            continue
        elif "increased Rarity of Items found in this Area" in output_line:
            continue
        elif output_line.startswith(("map", "Prefix", "Suffix")):
            # Skip irrelevant lines like 'map extra content weighting [0]'
            continue
        elif "increased Pack size" in output_line:
            insert_mod_group_file(mod_group)
            mod_group = []
            continue
        output_line = remove_preceding_mod_info(output_line)
        if output_line.startswith("Total"):
            # There should be one line with just 'Total', skip this line.
            continue
        output_line = replace_numbers_and_ranges(output_line)
        output_line = output_line.strip()
        if "Monsters cannot be Stunned" in output_line and "more Monster Life" in mod_group[0]:
            # Unwavering monsters has the % more monster life mod that comes along with it, which
            # is the same as another mod, so we need to remove it.
            mod_group[0] = output_line
        else:
            mod_group.append(output_line)


def generate_mod_group_name(mod_group: list) -> str:
    """
    generates a filesystem friendly name of a mod group.
    :param mod_group:
    :return:
    """
    return slugify(mod_group[-1])


def insert_mod_group_file(mod_group: list) -> None:
    """
    Create a file for a mod_group and insert the mods into it.
    :param mod_group:
    :return:
    """
    mod_group_name = generate_mod_group_name(mod_group)
    mod_group_file_path = output_folder + mod_group_name
    with open(log_file_path, "a") as log_file:
        if os.path.exists(mod_group_file_path):
            log_file.write("## EXISTS ## " + mod_group_name + "\n")
        else:
            with open(mod_group_file_path, "a") as mod_group_file:
                log_file.write("## CREATED ## " + mod_group_name + "\n")
                for line in mod_group:
                    log_file.write("## ADDED ## " + line + " to " + mod_group_name + "\n")
                    mod_group_file.write(line + "\n")


def replace_numbers_and_ranges(string_to_process: str) -> str:
    """
    Replaces all mod ranges (eg (10-20)%) and numbers with a hash.
    :param string_to_process:
    :return:
    """
    output = string_to_process
    output = re.sub(r'\(\d+–\d+\)', "#", output)
    output = re.sub(r'\(-\d+–-\d+\)', "-#", output)
    output = re.sub(r'\d+', "#", output)
    return output


def remove_preceding_mod_info(string_to_process: str) -> str:
    """
    Removes the preceding mod information from the input string, such as weightings and mod types.
    :param string_to_process:
    :return:
    """
    output = string_to_process.strip()
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
    if "increased Monster Cast Speed" in output:
        # This line actually has relevant numbers here, so we don't want to continue removing numbers.
        return output
    while re.match(r'^\d.*$', output):
        # Remove all numbers at the start of the line.
        output = output[1:]
    i = 0
    while i < len(mod_types):
        # Then remove all 'mod types' from the start of the line.
        if output.startswith(mod_types[i]):
            output = output.replace(mod_types[i], "", 1)
            i = 0
        else:
            i += 1
    if "less effect of Curses on Monsters" in output:
        # This line has relevant numbers after two numbers that need to be removed.
        output = output[2:]
        return output
    while re.match(r'^\d.*$', output):
        # Remove numbers that appear just after the mod types.
        output = output[1:]
    return output


if __name__ == "__main__":
    parse_poedb_list("./input_low.txt")
    parse_poedb_list("./input_mid.txt")
    parse_poedb_list("./input_high.txt")
