class MatchCollection:

    max_match_dict_size = 4

    def __init__(self) -> None:
        """
        Contains multiple dictionaries containing regular expressions and their matches.
        """
        super().__init__()
        self.one_way_matches = dict()
        self.two_way_matches = dict()
        self.three_way_matches = dict()
        self.four_way_matches = dict()

    def add_to_dict(self, key: frozenset[str], value: str) -> None:
        """
        Adds a key and value to the relevant dictionary of matches, depending on
        how many item are in the key. If the key already exists in the dictionary,
        this function checks if the value trying to be inserted is longer than
        what is already in the dictionary. If it is, the value is not added.
        :param key:
        :param value:
        :return:
        """
        match len(key):
            case 1:
                dict_to_add_to = self.one_way_matches
            case 2:
                dict_to_add_to = self.two_way_matches
            case 3:
                dict_to_add_to = self.three_way_matches
            case 4:
                dict_to_add_to = self.four_way_matches
            case _:
                return
        if key in dict_to_add_to:
            if len(dict_to_add_to[key]) < len(value):
                # If the regex that's already in as a match is shorter than what is trying
                # to be added, don't overwrite it.
                return
            # TODO: Add in a check to see which is shorter; what's being added or each item individually.
        dict_to_add_to[key] = value
