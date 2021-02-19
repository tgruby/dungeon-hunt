import town
from game_play import images, screen


def process(game, action):

    if action is None:
        return print_default(game)

    elif action.lower() == 'e':
        print("Hard games will lock the dungeon door behind the adventurer, and double the points for killing monsters.")
        # Setting game level
        game.game_mode = 'easy'
        game.current_controller = 'town'
        return town.process(game, None)

    elif action.lower() == 'h':
        print("Hard games will lock the dungeon door behind the adventurer, and double the points for killing monsters.")
        # Setting game level
        game.game_mode = 'hard'
        game.current_controller = 'town'
        return town.process(game, None)

    else:
        return print_default(game)


def print_default(game):
    # Print the default screen
    return screen.paint_one_pane(
        title_image=images.intro_scroll,
        contents="Do you want to play on easy mode or hard mode?  On hard mode monsters are harder and doors lock "
                 "behind you but you gain points faster.",
        contents_image=None,
        commands="(E)asy or (H)ard mode?",
        sound=None,
        delay=0,
        interaction_type='key_press',
        animation=None,
        game_id=game.game_id
    )