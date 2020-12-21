import importlib


class Game:
    # Constructor for our Game
    def __init__(self, game_id):
        self.game_id = game_id
        self.gamer_tag = None
        self.character = None
        self.dungeon = None
        self.current_controller = 'get_gamer_tag'
        self.score = 0
        self.game_over = False
        self.killed_by = None

    def calc_level_bonus(self, level_id, steps):
        #  Calculate updated score:
        level_bonus = (level_id + 1) * 2000
        step_deduction = steps * 10  # subtract the step costs.
        if step_deduction < level_bonus:
            level_bonus -= step_deduction
        else:
            level_bonus = 0
        self.score += level_bonus


def route(game, action):
    print("Calling " + game.current_controller + " with Action: " + str(action))
    controller = importlib.import_module('controller.' + game.current_controller, package=None)
    updated_screen = controller.process(game, action)

    if updated_screen is None:
        # set update_screen to an error message if blank response
        updated_screen = ["Error Processing Controller:",
                          "  controller..." + game.current_controller,
                          "  action......." + action,
                          "  game........" + game.game_id]

    return updated_screen
