import game_play.screen
from game_play import images, screen
from town import equipment_shop_sell, items
import town

commands = "Enter a (#) to purchase an item, (S)ell an item, or (L)eave Shop"
message = "Welcome to Bill's Equipment Emporium, mighty warrior!  Would you like to upgrade your shoddy " \
                  "equipment?"
image = images.weapons_shop_logo


# This function controls our interactions at the weapons store
def paint(game, msg):
    return screen.paint_two_panes(
        game=game,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=draw_buy_list(),
        sound=None,
        delay=0,
        interaction_type='key_press'
    )


def process(game, action):
    our_hero = game.character
    if action is None:
        return paint(game, message)

    # Leave and go back to the town
    if action.lower() == "l":
        game.current_controller = 'town'
        return town.process(game, None)

    # If Sell an item, enter another sub-controller
    if action.lower() == 's':
        game.current_controller = 'town.equipment_shop_sell'
        return equipment_shop_sell.process(game, None)

    if action.isdigit():
        return purchase_an_item(game, action)

    # If all else fails, just represent the current page.
    return paint(game, message)


def purchase_an_item(game, action):
    hero = game.character
    item_number_picked = int(action)
    if item_number_picked < len(items.equipment_shop_list):
        item = items.equipment_shop_list[item_number_picked]
        if item in hero.inventory:
            msg = "You already own that item!"
        elif hero.gold < item["cost"]:
            msg = "You don't have enough money for that!"
        else:
            hero.gold -= item["cost"]
            if item["type"] == "weapon":
                hero.equipped_weapon = item
            elif item["type"] == "armor":
                hero.equipped_armor = item
            elif item["type"] == "shield":
                hero.equipped_shield = item
            hero.inventory.append(item)
            msg = "You have purchased the %s." % item["name"]
    else:
        msg = "There is no weapon of that number!"

    return paint(game, msg)


def draw_buy_list():
    response = game_play.screen.medium_border + '\n'
    response += "  # | Item             | Type   | Dmg | Cost " + '\n'
    response += game_play.screen.medium_border + '\n'
    for number, e in enumerate(items.equipment_shop_list):
        response += game_play.screen.front_padding(str(number), 3) + " | " \
                    + game_play.screen.back_padding(e["name"], 16) + " | " \
                    + game_play.screen.front_padding(str(e["type"]), 6) + " | " \
                    + game_play.screen.front_padding(str(e["damage"]), 3) + " | " \
                    + game_play.screen.front_padding(str(round(e["cost"])), 4) + '\n'
    response += game_play.screen.medium_border + '\n'
    return response
