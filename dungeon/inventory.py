import game_play.screen
from game_play import images, screen
import dungeon
from town import potions

commands = "Enter a (#) to equip an item, or (L)eave"
message = "You open you pack and check your inventory..."
image = images.backpack_small


# This function controls accessing our hero's inventory
def paint(game, msg, sound):
    return screen.paint_two_panes(
        game=game,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=game_play.screen.list_inventory(game.character),
        sound=sound,
        delay=0,
        interaction_type='key_press'
    )


def process(game, action):
    if action is None:
        return paint(game, message, None)

    if action.lower() == 'l':
        game.current_controller = 'dungeon'
        return dungeon.process(game, None)

    if action.isdigit():
        return use_item(game, action)

    # If unknown action, show page again.
    return paint(game, message, None)


def use_item(game, action):
    sound = None
    hero = game.character
    item_number_picked = int(action)
    # Collapse Inventory Items returns a 2D Array with each element listed as [count, name, type, object]
    items_list = game_play.screen.collapse_inventory_items(hero)
    msg = ''
    if item_number_picked > len(items_list):
        return paint(game, "You do not have an item of that number!", sound)
    selected_item = items_list[item_number_picked - 1][4]
    if selected_item["type"] == "weapon":
        hero.equipped_weapon = selected_item
        msg = "You have equipped the %s." % selected_item["name"]
    elif selected_item["type"] == "armor":
        hero.equipped_armor = selected_item
        msg = "You have equipped the %s." % selected_item["name"]
    elif selected_item["type"] == "shield":
        hero.equipped_shield = selected_item
        msg = "You have equipped the %s." % selected_item["name"]
    elif selected_item["type"] == "potion":
        potions.use_potion(selected_item, game)
        sound = 'magic'
    else:
        msg = "You cannot equip that item!"

    return paint(game, msg, sound)
