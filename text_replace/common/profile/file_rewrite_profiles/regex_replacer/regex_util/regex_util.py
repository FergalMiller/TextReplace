from typing import List, Tuple, Match, Pattern


class GroupMatch(object):
    groups: List[Tuple[str, int, int]]

    def __init__(self): self.groups = []

    def get_value_of_group(self, group: int) -> str: return self.groups[group][0]

    def get_begin_position_of_group(self, group: int) -> int: return self.groups[group][1]

    def get_end_position_of_group(self, group: int) -> int: return self.groups[group][2]

    def add_group(self, group: Tuple[str, int, int]): self.groups.append(group)


class RegexUtil:
    @staticmethod
    def get_group_match(full_match: str, pattern: Pattern[str]) -> GroupMatch:
        group_match = GroupMatch()
        search: Match = pattern.search(full_match)
        for group in search.regs:
            end_position: int = group[1]
            begin_position: int = group[0]
            value = full_match[begin_position:end_position]
            as_tuple = (value, begin_position, end_position)
            group_match.add_group(as_tuple)
        return group_match

