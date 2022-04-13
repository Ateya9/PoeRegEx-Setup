import os
import re
from typing import List


class ModGroup:
    def __init__(self, mod_group_name: str) -> None:
        super().__init__()
        self.__mod_group_name = mod_group_name
        self.__mod_group_file_location = "./output/" + self.__mod_group_name
        if not os.path.exists(self.__mod_group_file_location):
            raise FileExistsError(mod_group_name + " doesn't exist.")
        self.__mods = []
        with open(self.__mod_group_file_location, "r") as mod_file:
            for line in mod_file:
                if line.strip():
                    self.__mods.append(line.strip())

    def __str__(self) -> str:
        return ', '.join(self.__mods)

    def check_for_regex_match(self, regex: str) -> bool:
        for mod in self.__mods:
            if re.search(regex, mod):
                return True
        return False

    def get_mods(self) -> list[str]:
        return self.__mods
