import view.screen
from model import items
from view import screen, images
from controller import town, equipment_shop_sell

commands = "Enter a (#) to purchase an item, (S)ell an item, or (L)eave Shop"
message = "Welcome to Bill's Equipment Emporium, mighty warrior!  Would you like to upgrade your shoddy " \
                  "equipment?"
image = images.weapons_shop_logo


# This function controls our interactions at the weapons store
def paint(our_hero, msg):
    return screen.paint_two_panes(
        hero=our_hero,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=draw_buy_list(),
        sound=None,
        delay=0,
        interaction_type='enter_press'
    )


def process(game, action):
    our_hero = game.character
    if action is None:
        return paint(our_hero, message)

    # Leave and go back to the town
    if action.lower() == "l":
        game.current_controller = 'town'
        return town.process(game, None)

    # If Sell an item, enter another sub-controller
    if action.lower() == 's':
        game.current_controller = 'equipment_shop_sell'
        return equipment_shop_sell.process(game, None)

    if action.isdigit():
        return purchase_an_item(our_hero, action)

    # If all else fails, just represent the current page.
    return paint(our_hero, message)


def purchase_an_item(our_hero, action):
    item_number_picked = int(action)
    if item_number_picked < len(items.equipment_shop_list):
        item = items.equipment_shop_list[item_number_picked]
        if item in our_hero.inventory:
            msg = "You already own that item!"
        elif our_hero.gold < item["cost"]:
            msg = "You don't have enough money for that!"
        else:
            our_hero.gold -= item["cost"]
            if item["type"] == "weapon":
                our_hero.equipped_weapon = item
            elif item["type"] == "armor":
                our_hero.equipped_armor = item
            elif item["type"] == "shield":
                our_hero.equipped_shield = item
            our_hero.inventory.append(item)
            msg = "You have purchased the %s." % item["name"]
    else:
        msg = "There is no weapon of that number!"

    return paint(our_hero, msg)


def draw_buy_list():
    response = view.screen.medium_border + '\n'
    response += "  # | Item         | Type   | Dmg | Cost " + '\n'
    response += view.screen.medium_border + '\n'
    for number, e in enumerate(items.equipment_shop_list):
        response += view.screen.front_padding(str(number), 3) + " | " \
                    + view.screen.back_padding(e["name"], 12) + " | " \
                    + view.screen.front_padding(str(e["type"]), 6) + " | " \
                    + view.screen.front_padding(str(e["damage"]), 3) + " | " \
                    + view.screen.front_padding(str(round(e["cost"])), 4) + '\n'
    response += view.screen.medium_border + '\n'
    return response
