import game_play.screen
from game_play import images, screen
from town import potions
import town

commands = "Enter a (#) to purchase an item, (L)eave Shop"
message = "Welcome to Janet's Potions!  Your gold is no good here, but for a few of your monster " \
              "'treasures' I can make you a potent elixir for your journeys."
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
        interaction_type='key_press'
    )


def process(game, action):
    print('Action: ' + str(action))
    our_hero = game.character

    if action is None:
        return paint(our_hero, message)

    # Leave and go back to the town
    if action.lower() == "l":
        game.current_controller = 'town'
        return town.process(game, None)

    # Attempt to buy an item
    if action.isdigit():
        return purchase_items(our_hero, action)

    # If we don't know what this action is, just represent the page
    return paint(our_hero, message)


def purchase_items(our_hero, action):
    item_number_picked = int(action)
    if item_number_picked <= len(potions.all_enchantments)-1:
        item = potions.all_enchantments[item_number_picked]

        if count_monster_parts(our_hero) < item["cost"]:
            msg = "You don't have enough monster parts for that!"
        else:
            take_monster_parts(our_hero, item["cost"])
            our_hero.inventory.append(item)
            msg = "You have purchased the %s." % item["name"]
    else:
        msg = "There is no item with that number!"

    return paint(our_hero, msg)


def draw_purchase_list():
    response = game_play.screen.medium_border + '\n'
    response += "  # | Item                           | Cost " + '\n'
    response += game_play.screen.medium_border + '\n'
    for number, e in enumerate(potions.all_enchantments):
        response += game_play.screen.front_padding(str(number), 3) + " | " \
                    + game_play.screen.back_padding(e["name"], 30) + " | " \
                    + game_play.screen.front_padding(str(e["cost"]), 4) + '\n'
    response += game_play.screen.medium_border + '\n'
    return response


def count_monster_parts(hero):
    count = 0
    for item in hero.inventory:
        if item['type'] == 'loot':
            count += 1
    return count


def take_monster_parts(hero, number):
    count = number
    for item in hero.inventory:
        if item['type'] == 'loot':
            hero.inventory.remove(item)
            count -= 1
            if count == 0:
                return
