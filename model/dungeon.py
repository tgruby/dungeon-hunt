from typing import List


class Dungeon:

    def __init__(self, levels):
        self.levels = levels
        self.completed_challenges: List[str] = []

    def complete_challenge(self, our_hero, type):
        level = our_hero.view.current_level_id
        x = our_hero.view.current_x
        y = our_hero.view.current_y
        # Mark the location of the challenge as complete so the next time we step here we don't launch a monster or
        # give another treasure
        self.completed_challenges.append(hash_challenge_location(level, x, y))
        # Subtract from the challenges count.  Once all challenges are complete, give user a skeleton key to go to
        # the next level.
        if type == 'treasure' or type == 'monster':
            self.levels[level]['challenge_count'] = self.levels[level].get('challenge_count') - 1

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
