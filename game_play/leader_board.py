from typing import List
from game_play import Game, screen, db, start_game


class Leaderboard:
    # Global Class Variables
    leaders: List[Game] = []

    def __init__(self, leaders):
        self.leaders = leaders

    # Return True if the character is alive, False if not.
    def update_leader(self, game):
        # Add the score to the top list.
        updated = False
        for idx, leader in enumerate(self.leaders):
            print("Compare: " + leader.game_id + " to " + game.game_id)
            if leader.game_id == game.game_id:
                print("Update Leader: " + game.game_id)
                self.leaders[idx] = game
                updated = True
        if not updated:
            print("Append Leader: " + game.game_id)
            self.leaders.append(game)

        # now sort the list and truncate if greater than 10
        self.leaders.sort(key=by_score, reverse=True)
        truncate_list(self.leaders, 15)


def truncate_list(sorted_list, limit):
    while len(sorted_list) > limit:
        del sorted_list[-1]


def by_score(game):
    return game.score


def process(game, action):
    db.init_db()
    lb = db.load_leaderboard()
    content = "         Rank | Character       | Status                     | Score " + '\n'
    content += '     <-------------------------------o-------------------------------> \n'
    # getting length of list
    length = len(lb.leaders)
    for i in range(length):
        content += "          " + \
                   screen.back_padding(str(i + 1), 3) + " | " + \
                   screen.back_padding(lb.leaders[i].character.name, 15) + " | " + \
                   screen.back_padding(lb.leaders[i].status, 26) + " | " + \
                   str(lb.leaders[i].score) + '\n'

    if action is None:
        return paint(content)

    if action.lower() == 's':
        # Create a new game
        return start_game.process(None, None)

    return paint(content)


def paint(scores):
    title = "H e r o ' s   o f   T h o r d o n"
    return screen.paint_one_pane(
        title_image=title,
        contents=None,
        contents_image=scores,
        commands="Press 'S' to start play...",
        sound=None,
        delay=0,
        interaction_type='key_press',
        animation=None,
        game_id=None
    )
