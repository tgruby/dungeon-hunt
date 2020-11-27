
class Leaderboard:
    # Global Class Variables
    top_ten = []

    # Return True if the character is alive, False if not.
    def add_leader(self, character):

        # If length is less than 10, just add it.
        if len(self.top_ten) < 10:
            self.top_ten.append(character)

        # else, if the last winner is less than the current character's xp add it.
        elif min(self.top_ten, key=by_experience_points) < character.experience_points:
            self.top_ten.append(character)

        # now just sort and truncate if greater than 10
        self.top_ten.sort(key=by_experience_points, reverse=True)
        truncate_list(self.top_ten, 10)


def by_experience_points(character):
    return character.experience_points


def truncate_list(sorted_list, limit):
    while len(sorted_list) > limit:
        del sorted_list[-1]
