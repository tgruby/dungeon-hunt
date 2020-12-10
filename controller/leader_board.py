import db
from view import screen, images


def process(game, action):
    db.init_db()
    lb = db.load_leaderboard()
    print("Leaderboard Length: " + str(len(lb.top_ten)))
    content = "  Rank | Gamer Tag                 | Score " + '\n'
    content += screen.medium_border + '\n'
    for i in range(len(lb.top_ten)):
        content += "   " + str(i+1) + "   | " + screen.back_padding(lb.top_ten[i].gamer_tag, 26) + " | " + \
                    str(lb.top_ten[i].score) + '\n'

    if action is not None:
        game.current_controller = 'start_game'

    return screen.paint_one_pane(
        title_image=images.title_1,
        contents=None,
        contents_image=content,
        commands="Press 'S' to start play...",
        sound=None,
        delay=0,
        interaction_type='key_press'
    )

