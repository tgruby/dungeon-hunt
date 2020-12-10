from view import screen, images
from controller import leader_board


def process(game, action):

    if action is None:
        return paint()

    game.gamer_tag = action
    game.current_controller = 'leader_board'
    return leader_board.process(game, None)


# Ask for Gamer Tag
def paint():
    return screen.paint_one_pane(
        title_image=images.title_1,
        contents='Please supply your Gamer Tag:',
        contents_image=None,
        commands=None,
        sound=None,
        delay=0,
        interaction_type='enter_press'
    )

