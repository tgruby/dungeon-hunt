import sys
import view.screen
from view import screen, images
from controller import router, enchantment_shop

commands = "Enter a (#) to sell an item, or (L)eave"
image = images.shop


# This function controls our interactions at the weapons store
def enter(our_hero):
    print("enchantment_shop_sell.enter")
    router.current_controller = sys.modules[__name__]

    return screen.paint(
        hero=our_hero,
        commands=commands,
        messages="Wonderful, we have been running low on hard to get items for our spells and potions!  What are you willing "
        "to part with? ",
        left_pane_content=image,
        right_pane_content=draw_sell_list(our_hero),
        sound=None,
        sleep=0
    )


def process(our_hero, action):
    print("enchantment_shop_sell.process: " + action)

    print(" +--> check if leave the shop...")
    # Leave and go back to the enchantment_shop
    if action.lower() == "l":
        return enchantment_shop.enter(our_hero)

    print(" +--> check if a digit...")
    if action.isdigit():
        return sell_items(our_hero, action)

    print(" +--> wtf, just represent the page...")
    return enter(our_hero)


# This function controls our interactions at the weapons store
def sell_items(our_hero, action):
    print("in sell items")
    item_number_picked = int(action)
    items_list = filtered_sell_list(our_hero)

    if item_number_picked > len(items_list) - 1 or item_number_picked < 0:
        msg = "You do not have an item of that number!"
    else:
        selected_item = items_list[item_number_picked][4]
        if selected_item["type"] == "loot":
            our_hero.gold += selected_item["cost"]
            our_hero.inventory.remove(selected_item)
            msg = "You sold %s for %d gold." % (selected_item["name"], selected_item["cost"])
        else:
            msg = "You cannot sell that item here!"

    return screen.paint(
        hero=our_hero,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=draw_sell_list(our_hero),
        sound=None,
        sleep=0
    )


def draw_sell_list(our_hero):
    items = filtered_sell_list(our_hero)
    response = view.screen.medium_border + '\n'
    response += "  # | Items            | Type   | Value " + '\n'
    response += view.screen.medium_border + '\n'
    for num, item in enumerate(items):
        response += view.screen.front_padding(str(num), 3) + " | " \
                    + view.screen.back_padding(str(item[0]) + " " + item[1], 16) + " | " \
                    + view.screen.front_padding(str(item[2]), 6) + " | " \
                    + view.screen.front_padding(str(item[3]), 4) + '\n'
    response += view.screen.medium_border + '\n'
    return response


# Create a Filtered list of only items we can sell in the enchantment shop
def filtered_sell_list(our_hero):
    filtered_list = []
    items_list = view.screen.collapse_inventory_items(our_hero)
    for item in items_list:
        if item[2] == "loot":
            filtered_list.append(item)

    return filtered_list
