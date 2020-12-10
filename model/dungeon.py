from typing import List


class Dungeon:

    def __init__(self, levels):
        self.levels = levels
        self.completed_challenges: List[str] = []

    def complete_challenge(self, our_hero):
        level = our_hero.view.current_level_id
        x = our_hero.view.current_x
        y = our_hero.view.current_y
        self.completed_challenges.append(hash_challenge_location(level, x, y))

    def is_challenge_completed(self, our_hero):
        level = our_hero.view.current_level_id
        x = our_hero.view.current_x
        y = our_hero.view.current_y
        if hash_challenge_location(level, x, y) in self.completed_challenges:
            return True
        return False

    def print_level(self, level_id):
        level = self.levels[level_id]
        print(level.get("map"))
        for row in level.get("maze"):
            line = ''
            for i in row:
                line += i
            print(line)


# standard mechanism for hashing the location and creating a location key.
def hash_challenge_location(level, x, y):
    location = str(level) + '-' + \
               str(x) + "-" + \
               str(y)
    return location
