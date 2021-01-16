import town
from town import items
import game_play.screen
from game_play import images, screen

commands = "(B)uy the next level map, or (L)eave the Shop"
message = "Welcome to Tina's Cartography, mighty warrior! Would you like to buy a map of the catacombs? They are " \
          "incredibly useful, and many warriors died to produce them! "
image = images.scroll


# This function controls our interactions at the weapons store
def paint(game):
    return screen.paint_two_panes(
        game=game,
        commands=commands,
        messages=message,
        left_pane_content=image,
        right_pane_content=draw_map_list(game),
        sound=None,
        delay=0,
        interaction_type='key_press'
    )


def process(game, action):
    if action is None:
        return paint(game)

    # Visit the Shop to buy stuff
    if action.lower() == 'b':
        return purchase_a_map(game, action)

    # Leave and go back to the town
    if action.lower() == "l":
        game.current_controller = 'town'
        return town.process(game, None)

    # Print the Shop page if we haven't returned yet.
    return paint(game)


def purchase_a_map(game, action):
    if game.character.gold < map_cost(game)[0]:
        msg = "You don't have enough money for that!"
    elif items.dungeon_map in game.character.inventory:
        msg = "You already have a map of the dungeon!"
    else:
        game.character.gold -= map_cost(game)[0]
        game.character.inventory.append(items.dungeon_map)
        msg = "You have boughten the " + items.dungeon_map["name"] + "!"

    return screen.paint_two_panes(
        game=game,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=draw_map_list(game),
        sound=None,
        delay=0,
        interaction_type='key_press'
    )


def draw_map_list(game):
    response = game_play.screen.medium_border + '\n'
    response += "   Item                         | Cost " + '\n'
    response += game_play.screen.medium_border + '\n'

    response += "   " \
                + game_play.screen.back_padding(items.dungeon_map["name"] + ", Level " + str(map_cost(game)[1]), 28) \
                + " | " + str(map_cost(game)[0]) + ' Gold\n'
    response += game_play.screen.medium_border + '\n'
    return response


def map_cost(game):
    level = game.dungeon.current_level_id + 1
    return (16 * level), level
