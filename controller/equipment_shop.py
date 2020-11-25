import sys
import view.screen
from model import items
from view import screen, images
from controller import router, town, equipment_shop_sell

commands = "Enter a (#) to purchase an item, (S)ell an item, or (L)eave Shop"
message = "Welcome to Bill's Equipment Emporium, mighty warrior!  Would you like to upgrade your shoddy " \
                  "equipment?"
image = images.weapons_shop_logo


# This function controls our interactions at the weapons store
def enter(our_hero):
    print("equipment_shop.enter")
    router.current_controller = sys.modules[__name__]

    return screen.paint(
        our_hero,
        commands,
        message,
        image,
        draw_buy_list(),
        None
    )


def process(our_hero, action):
    print("equipment_shop.process: " + action)

    # Leave and go back to the town
    if action.lower() == "l":
        router.current_controller = town
        return town.enter(our_hero)

    # If Sell an item, enter another sub-controller
    if action.lower() == 's':
        router.current_controller = equipment_shop_sell
        return equipment_shop_sell.enter(our_hero)

    if action.isdigit():
        return purchase_an_item(our_hero, action)

    # If all else fails, just represent the current page.
    return enter(our_hero)


def purchase_an_item(our_hero, action):
    item_number_picked = int(action)
    if item_number_picked < len(items.equipment_list):
        item = items.equipment_list[item_number_picked]
        if item in our_hero.inventory:
            message = "You already own that item!"
        elif our_hero.gold < item["cost"]:
            message = "You don't have enough money for that!"
        else:
            our_hero.gold -= item["cost"]
            if item["type"] == "weapon":
                our_hero.equipped_weapon = item
            elif item["type"] == "armor":
                our_hero.equipped_armor = item
            elif item["type"] == "shield":
                our_hero.equipped_shield = item
            our_hero.inventory.append(item)
            message = "You have purchased the %s." % item["name"]
    else:
        message = "There is no weapon of that number!"

    return screen.paint(
        our_hero,
        commands,
        message,
        image,
        draw_buy_list(),
        None
    )


def draw_buy_list():
    response = view.screen.medium_border + '\n'
    response += "  # | Item         | Type   | Dmg | Cost " + '\n'
    response += view.screen.medium_border + '\n'
    for number, e in enumerate(items.equipment_list):
        response += view.screen.front_padding(str(number), 3) + " | " \
                    + view.screen.back_padding(e["name"], 12) + " | " \
                    + view.screen.front_padding(str(e["type"]), 6) + " | " \
                    + view.screen.front_padding(str(e["damage"]), 3) + " | " \
                    + view.screen.front_padding(str(round(e["cost"])), 4) + '\n'
    response += view.screen.medium_border + '\n'
    return response
