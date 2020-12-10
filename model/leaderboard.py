
class Leaderboard:
    # Global Class Variables
    top_ten = []

    def __init__(self, leaders):
        self.top_ten = leaders

    # Return True if the character is alive, False if not.
    def add_leader(self, game):

        # Add the score to the top ten list.
        self.top_ten.append(game)

        # now sort the list and truncate if greater than 10
        self.top_ten.sort(key=by_score, reverse=True)
        truncate_list(self.top_ten, 10)


def truncate_list(sorted_list, limit):
    while len(sorted_list) > limit:
        del sorted_list[-1]


def by_score(game):
    return game.score