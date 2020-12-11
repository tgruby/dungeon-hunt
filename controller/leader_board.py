import db
import uuid
from view import screen


def process(game, action):
    db.init_db()
    lb = db.load_leaderboard()
    print("Leaderboard Length: " + str(len(lb.top_ten)))
    content = "  Rank | Gamer                     | Score " + '\n'
    content += screen.medium_border + '\n'
    # getting length of list
    length = len(lb.top_ten)
    for i in range(length):
        content += "   " + str(i+1) + "   | " + screen.back_padding(lb.top_ten[i].gamer_tag, 26) + " | " + \
                    str(lb.top_ten[i].score) + '\n'

    if action is None:
        return paint(content, None)

    if action.lower() == 's':
        # Create a new game
        game = db.load_game(str(uuid.uuid4()))
        game.current_controller = 'start_game'
        db.save_game(game.game_id, game)
        return paint(content, game.game_id)

    return paint(content, None)


def paint(scores, game_id):
    return screen.paint_one_pane(
        title_image='H I G H   S C O R E S',
        contents=None,
        contents_image=scores,
        commands="Press 'S' to start play...",
        sound=None,
        delay=0,
        interaction_type='key_press',
        game_id=game_id
    )

