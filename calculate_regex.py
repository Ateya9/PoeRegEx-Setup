import os
from mod_group import ModGroup
from match_collection import MatchCollection

output_folder = "./output/"


def check_requirements() -> bool:
    """
    Checks whether the output folder exists and if it has items in it.
    :return:
    """
    if not os.path.exists(output_folder):
        return False
    if len(os.listdir(output_folder)) <= 1:
        # No mods are in the folder.
        return False
    return True


def generate_mod_groups() -> list[ModGroup]:
    """
    Generates a ModGroup item for each file in output.
    :return:
    """
    output_list = []
    for mod_group_file in os.listdir(output_folder):
        if mod_group_file == "log.txt":
            continue
        current_mod_group = ModGroup(mod_group_file)
        output_list.append(current_mod_group)
    return output_list


def calculate_regex_matches(mod_group_to_test: ModGroup = None) -> MatchCollection:
    """
    Tests every potential regular expression against every ModGroup and adds them to a MatchCollection if
    relevant.
    :param mod_group_to_test:
    :return:
    """
    check_requirements()
    if mod_group_to_test is None:
        mod_groups = generate_mod_groups()
    else:
        mod_groups = [mod_group_to_test]
    test_mod_groups = generate_mod_groups()
    output = MatchCollection()
    for mod_group in mod_groups:
        potential_regexes = generate_potential_regexes(mod_group)
        for potential_regex in potential_regexes:
            matches = set()
            for test_mod_group in test_mod_groups:
                if len(matches) > output.max_match_dict_size:
                    # If we've already got too many matches, skip.
                    continue
                if test_mod_group.check_for_regex_match(potential_regex):
                    matches.add(test_mod_group.mod_group_name)
            if len(matches) > output.max_match_dict_size:
                # This if statement is unnecessary as the MatchCollection object
                # already handles this.
                continue
            output.add_to_dict(frozenset(matches), potential_regex)
    no_matches = get_unmatched_mods(mod_groups, output)
    if len(no_matches) > 0:
        for mod in no_matches:
            print(mod + " has no matches!")
    return output


def generate_potential_regexes(mod_group: ModGroup) -> list[str]:
    """
    Generates a list of potential regular expressions to be compared to each ModGroup.
    :param mod_group:
    :return:
    """
    # TODO: remove a 'potential' regex if it matches something in the banned words list.
    output = []
    # for each mod in the mod group, take incremental snips of letters (from 2 to 4
    # in length) to be used in the regular expressions. Eg 'more monster' would return
    # ['mo', 'or', 're', 'mor', 'ore' ...etc]
    for mod in mod_group.get_mods():

        # ---Single Snip---
        for snip_length in range(2, 9):
            # Take snips of varying lengths (2 to 8)
            for i in range(len(mod) - snip_length + 1):
                potential_regex = mod[i:i + snip_length]
                potential_regex = replace_invalid_regex_chars(potential_regex)
                output.append(potential_regex)

        # ---Double snip with space inbetween---
        # Take snips with space between them (varying space between but snips are always 2 long)
        for i in range(len(mod) - 3):
            space_between_snips = 0
            for y in range(i + 2, len(mod) - 1):
                first_snip = mod[i:i + 2]
                first_snip = replace_invalid_regex_chars(first_snip)
                second_snip = mod[y:y + 2]
                second_snip = replace_invalid_regex_chars(second_snip)
                match space_between_snips:
                    case 0:
                        inbetween_snip = ""
                    case 1:
                        inbetween_snip = "."
                    case _:
                        inbetween_snip = ".+"
                final_regex = first_snip + inbetween_snip + second_snip
                output.append(final_regex)
                space_between_snips += 1

        # ---Triple snip with space inbetween---
        # Same as above but 3 snips.
        for i in range(len(mod) - 5):
            space_between_left_snip = 0
            for y in range(i + 2, len(mod) - 3):
                space_between_right_snip = 0
                for x in range(y + 2, len(mod) - 1):
                    first_snip = mod[i:i + 2]
                    first_snip = replace_invalid_regex_chars(first_snip)
                    second_snip = mod[y:y + 2]
                    second_snip = replace_invalid_regex_chars(second_snip)
                    third_snip = mod[x:x + 2]
                    third_snip = replace_invalid_regex_chars(third_snip)
                    match space_between_left_snip:
                        case 0:
                            inbetween_left_snip = ""
                        case 1:
                            inbetween_left_snip = "."
                        case _:
                            inbetween_left_snip = ".+"
                    match space_between_right_snip:
                        case 0:
                            inbetween_right_snip = ""
                        case 1:
                            inbetween_right_snip = "."
                        case _:
                            inbetween_right_snip = ".+"
                    final_regex = first_snip + inbetween_left_snip + second_snip + inbetween_right_snip + third_snip
                    output.append(final_regex)
                    space_between_right_snip += 1
                space_between_left_snip += 1
    return output


def replace_invalid_regex_chars(input_regex: str) -> str:
    """
    Replaces invalid characters in the regular expressions. Such as; makes sure any plus signs
    are preceded by a backslash.
    :param input_regex:
    :return:
    """
    output = input_regex
    output = output.replace("+", r"\+")
    output = output.replace("#", "\\d+")
    return output


def get_unmatched_mods(mod_groups: list[ModGroup], match_collection: MatchCollection) -> list[str]:
    """
    Finds any ModGroups that don't have a one way match in the supplied MatchCollection.
    :param mod_groups:
    :param match_collection:
    :return:
    """
    output = []
    for mod in mod_groups:
        if frozenset({mod.mod_group_name}) not in match_collection.one_way_matches:
            output.append(mod.mod_group_name)
    return output


if __name__ == "__main__":
    # Testing
    matches = calculate_regex_matches()
    print("####" + str(len(matches.one_way_matches)) + " one way matches. ####")
    for k, v in matches.one_way_matches.items():
        print(f"{k} : '{v}'")
    print("####" + str(len(matches.two_way_matches)) + " two way matches. ####")
    for k, v in matches.two_way_matches.items():
        print(f"{k} : '{v}'")
    print("####" + str(len(matches.three_way_matches)) + " three way matches. ####")
    for k, v in matches.three_way_matches.items():
        print(f"{k} : '{v}'")
    print("####" + str(len(matches.four_way_matches)) + " four way matches. ####")
    for k, v in matches.four_way_matches.items():
        print(f"{k} : '{v}'")
