import sys
import view.screen
from view import screen, images
from model import enchantments
from controller import router, town, enchantment_shop_sell

commands = "Enter a (#) to purchase an item, (S)ell an Item, (L)eave Shop"
message = "Welcome to Janet's Enchantments!  Would you like me to use some of your monster " \
              "'treasures' to make you potent elixir for your journeys?"
image = images.shop

# TODO: Create more Scrolls for casting spells to affect monsters


# This function controls our interactions at the weapons store
def enter(our_hero):
    print("enchantment_shop.enter")
    router.current_controller = sys.modules[__name__]

    return screen.paint(
        hero=our_hero,
        commands=commands,
        messages=message,
        left_pane_content=image,
        right_pane_content=draw_purchase_list(),
        sound=None,
        sleep=100
    )


def process(our_hero, action):
    print("enchantment_shop.process: " + action)

    # Leave and go back to the town
    if action.lower() == "l":
        return town.enter(our_hero)

    # Go to the sell controller
    if action.lower() == 's':
        return enchantment_shop_sell.enter(our_hero)

    # Attempt to buy an item
    if action.isdigit():
        return purchase_items(our_hero, action)

    # If we don't know what this action is, just represent the page
    return enter(our_hero)


def purchase_items(our_hero, action):
    item_number_picked = int(action)
    if item_number_picked <= len(enchantments.all_enchantments)-1:
        item = enchantments.all_enchantments[item_number_picked]
        if our_hero.gold < item["cost"]:
            message = "You don't have enough money for that!"
        else:
            our_hero.gold -= item["cost"]
            our_hero.inventory.append(item)
            message = "You have purchased the %s." % item["name"]
    else:
        message = "There is no item with that number!"

    return screen.paint(
        hero=our_hero,
        commands=commands,
        messages=message,
        left_pane_content=image,
        right_pane_content=draw_purchase_list(),
        sound=None,
        sleep=100
    )


def draw_purchase_list():
    response = view.screen.medium_border + '\n'
    response += "  # | Item                           | Cost " + '\n'
    response += view.screen.medium_border + '\n'
    for number, e in enumerate(enchantments.all_enchantments):
        response += view.screen.front_padding(str(number), 3) + " | " \
                    + view.screen.back_padding(e["name"], 30) + " | " \
                    + view.screen.front_padding(str(e["cost"]), 4) + '\n'
    response += view.screen.medium_border + '\n'
    return response
