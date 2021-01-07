import game_play.screen
from game_play import images, screen
from town import equipment_shop

commands = "Enter a (#) to sell an item, or (L)eave."
message = "Wonderful, we have been running low on good hardware!  What are you " \
          "willing to part with? "
image = images.weapons_shop_logo


# This function controls our interactions at the weapons store
def paint(game, msg):
    return screen.paint_two_panes(
        game=game,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=draw_sell_list(game.character),
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
        game.current_controller = 'town.equipment_shop'
        return equipment_shop.process(game, None)

    # If Sell an item, enter another sub-controller
    if action.isdigit():
        return sell_items(game, action)

    # If we don't know, just reshow page.
    return paint(game, message)


def sell_items(game, action):
    hero = game.character
    item_number_picked = int(action)
    items_list = filtered_sell_list(hero)
    if item_number_picked > len(items_list)-1 or item_number_picked < 0:
        msg = "You do not have an item of that number!"
    else:
        selected_item = items_list[item_number_picked][4]
        selected_item_quantity = items_list[item_number_picked][0]
        if selected_item["type"] == "weapon" or selected_item["type"] == "armor" or selected_item["type"] == "shield":
            if selected_item["name"] == hero.equipped_weapon["name"] and selected_item_quantity == 1:
                msg = "You cannot sell equipped items!"
            elif hero.equipped_armor is not None and selected_item["name"] == hero.equipped_armor["name"] and selected_item_quantity == 1:
                msg = "You cannot sell equipped items!"
            elif hero.equipped_shield is not None and selected_item["name"] == hero.equipped_shield["name"] and selected_item_quantity == 1:
                msg = "You cannot sell equipped items!"
            else:
                hero.gold += selected_item["cost"] / 2
                hero.inventory.remove(selected_item)
                msg = "You sold %s for %d gold." % (selected_item["name"], selected_item["cost"]/2)
        else:
            msg = "You cannot sell that item here!"

    return paint(game, msg)


def draw_sell_list(our_hero):
    items = filtered_sell_list(our_hero)
    response = game_play.screen.medium_border + '\n'
    response += "  # | Items            | Type   | Value " + '\n'
    response += game_play.screen.medium_border + '\n'
    for num, item in enumerate(items):
        response += game_play.screen.front_padding(str(num), 3) + " | " \
                    + game_play.screen.back_padding(str(item[0]) + " " + item[1], 16) + " | " \
                    + game_play.screen.front_padding(str(item[2]), 6) + " | " \
                    + game_play.screen.front_padding(str(round(item[3] / 2)), 4) + '\n'
    response += game_play.screen.medium_border + '\n'
    return response


# Create a Filtered list of only items we can sell in the potion shop
def filtered_sell_list(our_hero):
    filtered_list = []
    items_list = game_play.screen.collapse_inventory_items(our_hero)
    for item in items_list:
        if item[2] == 'armor' or item[2] == 'shield' or item[2] == 'weapon':
            filtered_list.append(item)

    return filtered_list
