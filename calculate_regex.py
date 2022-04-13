import os
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


def output_regexes() -> None:
    check_requirements()
    mod_groups = generate_mod_groups()
    one_way_matches = dict()
    two_way_matches = dict()
    three_way_matches = dict()
    # TODO: Check banned words list
    number_of_matches = 0
    regex_iterator = 0
    regex_length = 2
    confirmed_regex = ""
    for mod_group in mod_groups:
        for mod in mod_group.get_mods():

            potential_regex = mod[regex_iterator:regex_length]
            for test_mod_group in mod_groups:
                pass


def generate_potential_regexes(mod_group: ModGroup) -> list[str]:
    output = []
    # for each mod in the mod group, take incremental snips of letters (from 2 to 4 in length) to be used
    # in the regular expressions. Eg 'more monster' would return ['mo', 'or', 're', 'mor', 'ore' ...etc]
    for mod in mod_group.get_mods():
        for snip_length in range(2, 5):
            # Take snips of varying lengths (2 to 4)
            for i in range(len(mod) - snip_length + 1):
                potential_regex = mod[i:i + snip_length]
                potential_regex = potential_regex.replace("#", "\\d*")
                output.append(potential_regex)
        # Take snips with space between them (varying space between but snips are always 2 long)
        for i in range(len(mod) - 1):
            space_between_snips = 0
            for y in range(i + 2, len(mod) - 1):
                first_snip = mod[i:i + 2]
                first_snip = first_snip.replace("#", "\\d*")
                second_snip = mod[y:y + 2]
                second_snip = second_snip.replace("#", "\\d*")
                match space_between_snips:
                    case 0:
                        inbetween_snip = ""
                    case 1:
                        inbetween_snip = "."
                    case _:
                        inbetween_snip = ".{" + str(space_between_snips) + "}"
                final_regex = first_snip + inbetween_snip + second_snip
                output.append(final_regex)
                space_between_snips += 1
    return output


if __name__ == "__main__":
    # output_regexes()
    mod_groups = generate_mod_groups()
    print(mod_groups[1].get_mods()[0])
    potential_regexes = generate_potential_regexes(mod_groups[1])
    print(potential_regexes)
