import view.screen
from view import screen, images
from model import enchantments
from controller import town, enchantment_shop_sell

commands = "Enter a (#) to purchase an item, (S)ell an Item, (L)eave Shop"
message = "Welcome to Janet's Enchantments!  Would you like me to use some of your monster " \
              "'treasures' to make you potent elixir for your journeys?"
image = images.shop


# This function controls our interactions at the weapons store
def paint(our_hero, msg):
    return screen.paint_two_panes(
        hero=our_hero,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=draw_purchase_list(),
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

    # Go to the sell controller
    if action.lower() == 's':
        game.current_controller = 'enchantment_shop_sell'
        return enchantment_shop_sell.process(game, None)

    # Attempt to buy an item
    if action.isdigit():
        return purchase_items(our_hero, action)

    # If we don't know what this action is, just represent the page
    return print(our_hero, message)


def purchase_items(our_hero, action):
    item_number_picked = int(action)
    if item_number_picked <= len(enchantments.all_enchantments)-1:
        item = enchantments.all_enchantments[item_number_picked]
        if our_hero.gold < item["cost"]:
            msg = "You don't have enough money for that!"
        else:
            our_hero.gold -= item["cost"]
            our_hero.inventory.append(item)
            msg = "You have purchased the %s." % item["name"]
    else:
        msg = "There is no item with that number!"

    return paint(our_hero, msg)


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
