import importlib


# Game Object.  Every Game has this object.
class Game:
    # Constructor for our Game
    def __init__(self, game_id):
        self.game_id = game_id
        self.gamer_tag = None
        self.game_mode = 'easy'
        self.character = None
        self.dungeon = None
        self.score = 0
        self.game_over = False
        self.status = None
        self.current_controller = None

    def calc_score_level_bonus(self):
        #  Calculate updated score:
        level_step_goal = self.dungeon.current_level_id * 100
        if self.character.step_count > level_step_goal:
            level_bonus = 0
        else:
            if self.game_mode == 'hard':
                level_bonus = self.dungeon.current_level_id * 200
            else:
                level_bonus = self.dungeon.current_level_id * 100
        self.score += level_bonus
        self.character.step_count = 0
        return level_bonus

    def calc_hp_bonus(self):
        #  Calculate updated hp:
        monsters_killed = self.dungeon.current_level["monsters_killed"]
        self.character.max_hit_points += monsters_killed
        self.character.hit_points += monsters_killed
        if self.character.hit_points > self.character.max_hit_points:
            self.character.hit_points = self.character.max_hit_points
        return monsters_killed

    def calc_boss_bonus(self):
        #  Calculate updated hp:
        boss_bonus = self.dungeon.current_level_id * 100
        self.score += boss_bonus
        return boss_bonus

    def increment_treasure_score(self):
        self.score += 10  # Obtain 10 points per treasure

    def increment_monster_score(self):
        # Increase Score for killing monsters.  The higher the level, the more points.
        if self.game_mode == 'hard':
            # Add extra points for being in hard mode
            self.score += self.dungeon.current_level_id * 20
        else:
            self.score += self.dungeon.current_level_id * 10


def route(game, action):
    print("Calling " + game.current_controller + " with Action: " + str(action))
    controller = importlib.import_module(game.current_controller, package=None)
    updated_screen = controller.process(game, action)

    if updated_screen is None:
        # set update_screen to an error message if blank response
        updated_screen = ["Error Processing Controller:",
                          "  controller..." + game.current_controller,
                          "  action......." + action,
                          "  game........" + game.game_id]

    return updated_screen
