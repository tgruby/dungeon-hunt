from game_play import images, screen, db
import town


def process(game, action):

    if action is None:
        return paint(game)

    # Visit the Shop to buy stuff
    if action.lower() == "x":
        game.current_controller = 'town'
        return town.process(game, None)

    # Something else?
    return paint(game)


def paint(game):

    db.init_db()
    lb = db.load_leaderboard()
    content = "  H e r o ' s   o f   T h o r d o n\n\n\n"
    content += '  Rank | Character       | Score\n'
    content += '<------o-----------------o--------> \n'
    # getting length of list
    for i in range(len(lb.leaders)):
        content += "   " + \
                   screen.back_padding(str(i + 1), 3) + " | " + \
                   screen.back_padding(lb.leaders[i].gamer_tag, 15) + " | " + \
                   str(lb.leaders[i].score) + '\n'

    return screen.paint_two_panes(
        game=game,
        commands="E(x)it",
        messages=None,
        left_pane_content=images.shield,
        right_pane_content=content,
        sound=None,
        delay=0,
        interaction_type='key_press'
    )
