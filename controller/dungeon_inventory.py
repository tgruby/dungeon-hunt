import view.screen
from view import screen, images
from controller import dungeon
from model import potions

commands = "Enter a (#) to equip an item, or (C)lose Pack"
message = "You open you pack and check your inventory..."
image = images.backpack_small


# This function controls accessing our hero's inventory
def paint(our_hero, msg):
    return screen.paint_two_panes(
        hero=our_hero,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=view.screen.list_inventory(our_hero),
        sound=None,
        delay=0,
        interaction_type='enter_press'
    )


def process(game, action):
    our_hero = game.character
    if action is None:
        return paint(our_hero, message)

    if action.lower() == 'c':
        game.current_controller = 'dungeon'
        return dungeon.process(game, None)

    if action.isdigit():
        return use_item(game, action)

    # If unknown action, show page again.
    return paint(our_hero, message)


def use_item(game, action):
    our_hero = game.character
    item_number_picked = int(action)
    # Collapse Inventory Items returns a 2D Array with each element listed as [count, name, type, object]
    items_list = view.screen.collapse_inventory_items(our_hero)
    msg = ''
    if item_number_picked > len(items_list):
        return paint(our_hero, "You do not have an item of that number!")
    selected_item = items_list[item_number_picked - 1][4]
    if selected_item["type"] == "weapon":
        our_hero.equipped_weapon = selected_item
        msg = "You have equipped the %s." % selected_item["name"]
    elif selected_item["type"] == "armor":
        our_hero.equipped_armor = selected_item
        msg = "You have equipped the %s." % selected_item["name"]
    elif selected_item["type"] == "shield":
        our_hero.equipped_shield = selected_item
        msg = "You have equipped the %s." % selected_item["name"]
    elif selected_item["type"] == "potion":
        potions.use_potion(selected_item, game)
    else:
        msg = "You cannot equip that item!"

    return paint(our_hero, msg)
