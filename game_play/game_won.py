from game_play import db, screen, images


def process(game, action):

    title_image = 'T H E   T O W N   R E J O I C E S ! ! !'

    # Update the Leaderboard
    game.status = "Won!!!!"
    game.game_over = True
    lb = db.load_leaderboard()
    lb.update_leader(game)
    db.save_leaderboard(lb)

    return screen.paint_one_pane(
        title_image=title_image,
        contents='The town rejoices as the dragon is vanquished, their labyrinth drain of evil monsters and the town returns to a peaceful existence.  You are declared Lord of Thordon, granted the local castle, and reign Thordon and the surrounding lands for many years.  Well done, Warrior!',
        contents_image=images.castle,
        commands="Hit any key to continue...",
        sound='level-complete',
        delay=2000,
        animation='confetti',
        interaction_type='key_press',
        game_id=game.game_id
    )
