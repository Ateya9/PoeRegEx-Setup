import os
import sys
from mod_group import ModGroup

output_folder = "./output/"


def check_requirements() -> bool:
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    if len(os.listdir(output_folder)) <= 1:
        # No mods are in the folder.
        return False
    return True


def generate_mod_groups() -> list[ModGroup]:
    output_list = []
    for mod_group_file in os.listdir(output_folder):
        if mod_group_file == "log.txt":
            continue
        current_mod_group = ModGroup(mod_group_file)
        output_list.append(current_mod_group)
    return output_list


def generate_regex() -> None:
    check_requirements()
    mod_groups = generate_mod_groups()
    one_way_matches = dict()
    two_way_matches = dict()
    three_way_matches = dict()


if __name__ == "__main__":
    generate_regex()
