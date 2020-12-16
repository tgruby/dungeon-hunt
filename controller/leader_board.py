import db
from controller import start_game
from view import screen


class Leaderboard:
    # Global Class Variables
    high_scores = []

    def __init__(self, leaders):
        self.high_scores = leaders

    # Return True if the character is alive, False if not.
    def add_leader(self, game):
        # Add the score to the top ten list.
        self.high_scores.append(game)

        # now sort the list and truncate if greater than 10
        self.high_scores.sort(key=by_score, reverse=True)
        truncate_list(self.high_scores, 15)


def truncate_list(sorted_list, limit):
    while len(sorted_list) > limit:
        del sorted_list[-1]


def by_score(game):
    return game.score


def process(game, action):
    db.init_db()
    lb = db.load_leaderboard()
    print("Leaderboard Length: " + str(len(lb.high_scores)))
    content = "  Rank | Gamer                | Killed By              | Score " + '\n'
    content += '<=============================<o>==============================>\n'
    # getting length of list
    length = len(lb.high_scores)
    for i in range(length):
        content += "   " + \
                   screen.back_padding(str(i + 1), 3) + " | " + \
                   screen.back_padding(lb.high_scores[i].gamer_tag, 20) + " | " + \
                   screen.back_padding(lb.high_scores[i].killed_by, 22) + " | " + \
                   str(lb.high_scores[i].score) + '\n'

    if action is None:
        return paint(content)

    if action.lower() == 's':
        # Create a new game
        return start_game.process(None, None)

    return paint(content)


def paint(scores):
    return screen.paint_one_pane(
        title_image='H I G H   S C O R E S',
        contents=None,
        contents_image=scores,
        commands="Press 'S' to start play...",
        sound=None,
        delay=0,
        interaction_type='key_press',
        game_id=None
    )
