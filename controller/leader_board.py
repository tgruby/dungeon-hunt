import db
from controller import start_game
from view import screen


def process(game, action):
    db.init_db()
    lb = db.load_leaderboard()
    print("Leaderboard Length: " + str(len(lb.top_ten)))
    content = "  Rank | Gamer                      | Score " + '\n'
    content += screen.medium_border + '\n'
    # getting length of list
    length = len(lb.top_ten)
    for i in range(length):
        content += "   " + \
                    screen.back_padding(str(i+1), 3) + " | " + \
                    screen.back_padding(lb.top_ten[i].gamer_tag, 26) + " | " + \
                    str(lb.top_ten[i].score) + '\n'

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

