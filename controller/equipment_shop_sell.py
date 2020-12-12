import view.screen
from view import screen, images
from controller import equipment_shop

commands = "Enter a (#) to sell an item, or (L)eave."
message = "Wonderful, we have been running low on good hardware!  What are you " \
          "willing to part with? "
image = images.weapons_shop_logo


# This function controls our interactions at the weapons store
def paint(our_hero, msg):
    return screen.paint_two_panes(
        hero=our_hero,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=draw_sell_list(our_hero),
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
        game.current_controller = 'equipment_shop'
        return equipment_shop.process(game, None)

    # If Sell an item, enter another sub-controller
    if action.isdigit():
        return sell_items(our_hero, action)

    # If we don't know, just reshow page.
    return paint(our_hero, message)


def sell_items(our_hero, action):
    item_number_picked = int(action)
    items_list = filtered_sell_list(our_hero)
    if item_number_picked > len(items_list)-1 or item_number_picked < 0:
        msg = "You do not have an item of that number!"
    else:
        selected_item = items_list[item_number_picked][4]
        selected_item_quantity = items_list[item_number_picked][0]
        if selected_item["type"] == "weapon" or selected_item["type"] == "armor" or selected_item["type"] == "shield":
            if selected_item["name"] == our_hero.equipped_weapon["name"] and selected_item_quantity == 1:
                msg = "You cannot sell equipped items!"
            elif our_hero.equipped_armor is not None and selected_item["name"] == our_hero.equipped_armor["name"] and selected_item_quantity == 1:
                msg = "You cannot sell equipped items!"
            elif our_hero.equipped_shield is not None and selected_item["name"] == our_hero.equipped_shield["name"] and selected_item_quantity == 1:
                msg = "You cannot sell equipped items!"
            else:
                our_hero.gold += selected_item["cost"] / 2
                our_hero.inventory.remove(selected_item)
                msg = "You sold %s for %d gold." % (selected_item["name"], selected_item["cost"]/2)
        else:
            msg = "You cannot sell that item here!"

    return paint(our_hero, msg)


def draw_sell_list(our_hero):
    items = filtered_sell_list(our_hero)
    response = view.screen.medium_border + '\n'
    response += "  # | Items            | Type   | Value " + '\n'
    response += view.screen.medium_border + '\n'
    for num, item in enumerate(items):
        response += view.screen.front_padding(str(num), 3) + " | " \
                    + view.screen.back_padding(str(item[0]) + " " + item[1], 16) + " | " \
                    + view.screen.front_padding(str(item[2]), 6) + " | " \
                    + view.screen.front_padding(str(round(item[3] / 2)), 4) + '\n'
    response += view.screen.medium_border + '\n'
    return response


# Create a Filtered list of only items we can sell in the enchantment shop
def filtered_sell_list(our_hero):
    filtered_list = []
    items_list = view.screen.collapse_inventory_items(our_hero)
    for item in items_list:
        if item[2] == 'armor' or item[2] == 'shield' or item[2] == 'weapon':
            filtered_list.append(item)

    return filtered_list
