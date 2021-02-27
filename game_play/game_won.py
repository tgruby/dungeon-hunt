from game_play import db, screen


def process(game, action):

    # Update the Leaderboard
    game.status = "Won the Game!!!!"
    game.game_over = True
    lb = db.load_leaderboard()
    lb.update_leader(game)
    db.save_leaderboard(lb)

    return screen.paint_winning_screen(game.game_id)
