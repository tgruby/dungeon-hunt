import view.screen
from model import maps
from view import screen, images
from controller import town

commands = "Enter a (#) to purchase an item, (L)eave Shop"
message = "Welcome to Tina's Cartography, mighty warrior! Would you like to buy a map of the dungeon? They are " \
          "incredibly useful, and many warriors died to produce them! "
image = images.scroll


# This function controls our interactions at the weapons store
def paint(hero):
    return screen.paint_two_panes(
        hero=hero,
        commands=commands,
        messages=message,
        left_pane_content=image,
        right_pane_content=draw_map_list(),
        sound=None,
        delay=0,
        interaction_type='enter_press'
    )


def process(game, action):
    character = game.character
    if action is None:
        return paint(character)

    # Visit the Shop to buy stuff
    if action.isdigit():
        return purchase_a_map(character, action)

    # Leave and go back to the town
    if action.lower() == "l":
        game.current_controller = 'town'
        return town.process(game, None)

    # Print the Shop page if we haven't returned yet.
    return paint(character)


def purchase_a_map(our_hero, action):
    if action.isdigit():
        number_picked = int(action)
        if number_picked < len(maps.map_list):
            m = maps.map_list[number_picked]
            if m in our_hero.inventory:
                msg = "You already own that map!"
            elif our_hero.gold < m["cost"]:
                msg = "You don't have enough money for that!"
            else:
                our_hero.gold -= m["cost"]
                our_hero.inventory.append(m)
                msg = "You have boughten the " + m["name"] + "!"
        else:
            msg = "There is no map for that number!"
    else:
        msg = "You need to specify a number."

    return screen.paint_two_panes(
        hero=our_hero,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=draw_map_list(),
        sound=None,
        delay=0,
        interaction_type='enter_press'
    )


def draw_map_list():
    response = view.screen.medium_border + '\n'
    response += "  # | Item              |      Cost " + '\n'
    response += view.screen.medium_border + '\n'
    for number, m in enumerate(maps.map_list):
        response += view.screen.front_padding(str(number), 3) + " | " \
                    + view.screen.back_padding(m["name"], 17) + " | " \
                    + view.screen.front_padding(str(m["cost"]), 4) + ' Gold\n'
    response += view.screen.medium_border + '\n'
    return response
