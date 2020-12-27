from typing import List


class Dungeon:

    def __init__(self, levels):
        self.levels = levels
        self.completed_challenges: List[str] = []

    def complete_challenge(self, our_hero, challenge_type):
        level = our_hero.view.current_level_id
        x = our_hero.view.current_x
        y = our_hero.view.current_y
        # Mark the location of the challenge as complete so the next time we step here we don't launch a monster or
        # give another treasure
        self.completed_challenges.append(hash_challenge_location(level, x, y))
        # Subtract from the treasure count.  Once all challenges are complete, give user a skeleton key to go to
        # the next level.
        if challenge_type == 'treasure':
            self.levels[level]['treasures_collected'] += 1
        if challenge_type == 'trap':
            self.levels[level]['traps_triggered'] += 1
        if challenge_type == 'monster':
            self.levels[level]['monsters_killed'] += 1

    def is_challenge_completed(self, our_hero):
        level = our_hero.view.current_level_id
        x = our_hero.view.current_x
        y = our_hero.view.current_y
        if hash_challenge_location(level, x, y) in self.completed_challenges:
            return True
        return False

    def are_all_treasures_collected(self, level_id):
        return self.levels[level_id]['treasure_count'] - self.levels[level_id]['treasures_collected'] == 0

    def is_level_locked(self, level_id):
        return self.levels[level_id]['level_locked']

    def unlock_level(self, level_id):
        self.levels[level_id]['level_locked'] = False

    # Add method to determine if we should skip walking through the level (all challenges completed and the next
    # level is unlocked.
    def should_skip_walking_through_level(self, level_id):
        return self.are_all_treasures_collected(level_id) and not self.is_level_locked(level_id + 1)

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
