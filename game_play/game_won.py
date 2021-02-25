from game_play import db, screen, images


def process(game, action):

    title_image = 'T H E   T O W N   R E J O I C E S ! ! !'

    # Update the Leaderboard
    game.status = "Won the Game!!!!"
    game.game_over = True
    lb = db.load_leaderboard()
    lb.update_leader(game)
    db.save_leaderboard(lb)

    return screen.paint_winning_screen(game.game_id)
