class MatchCollection:

    max_match_dict_size = 3

    def __init__(self) -> None:
        super().__init__()
        self.one_way_matches = dict()
        self.two_way_matches = dict()
        self.three_way_matches = dict()

    def add_to_dict(self, key: set, value: str) -> None:
        match len(key):
            case 1:
                dict_to_add_to = self.one_way_matches
            case 2:
                dict_to_add_to = self.two_way_matches
            case 3:
                dict_to_add_to = self.three_way_matches
            case _:
                return
        if key in dict_to_add_to:
            if len(dict_to_add_to[key]) < len(value):
                # If the regex that's already in as a match is shorter than what is trying
                # to be added, don't overwrite it.
                return
        dict_to_add_to[key] = value
