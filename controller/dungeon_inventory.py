import sys
import random

import view.screen
from view import screen, images
from controller import router, dungeon

commands = "Enter a (#) to equip an item, or (C)lose Pack"
message = "You open you pack and check your inventory..."
image = images.backpack_small


# This function controls accessing our hero's inventory
def enter(our_hero):
    print("inventory.enter")
    router.current_controller = sys.modules[__name__]

    return screen.paint(
        our_hero,
        commands,
        message,
        image,
        view.screen.list_inventory(our_hero),
        None
    )


def process(our_hero, action):
    print("inventory.process: " + action)

    if action.lower() == 'c':
        return dungeon.enter(our_hero)

    if action.isdigit():
        return use_item(our_hero, action)

    # If unknown action, show page again.
    return enter(our_hero)


def use_item(our_hero, action):
    item_number_picked = int(action)
    # Collapse Inventory Items returns a 2D Array with each element listed as [count, name, type, object]
    items_list = view.screen.collapse_inventory_items(our_hero)
    if item_number_picked > len(items_list):
        return screen.paint(
            our_hero,
            commands,
            "You do not have an item of that number!",
            image,
            view.screen.list_inventory(our_hero),
            None
        )
    selected_item = items_list[item_number_picked - 1][4]
    if selected_item["type"] == "weapon":
        our_hero.equipped_weapon = selected_item
        message = "You have equipped the %s." % selected_item["name"]
    elif selected_item["type"] == "armor":
        our_hero.equipped_armor = selected_item
        message = "You have equipped the %s." % selected_item["name"]
    elif selected_item["type"] == "shield":
        our_hero.equipped_shield = selected_item
        message = "You have equipped the %s." % selected_item["name"]
    elif selected_item["type"] == "potion":
        if our_hero.hit_points == our_hero.max_hit_points:
            message = "You don't need that right now."
        else:
            healing = random.randint(4, selected_item["max_hit_points"])
            if our_hero.hit_points + healing > our_hero.max_hit_points:
                our_hero.hit_points = our_hero.max_hit_points
            else:
                our_hero.hit_points += healing
            our_hero.inventory.remove(selected_item)
            message = "You drank the %s and a warm fuzzy feeling comes over you." % selected_item["name"]
    else:
        message = "You cannot equip that item!"

    return screen.paint(
        our_hero,
        commands,
        message,
        image,
        view.screen.list_inventory(our_hero),
        None
    )
