import sys
import view.screen
from view import screen, images
from controller import dungeon, cartography_shop, equipment_shop, temple, enchantment_shop, router

commands = "(E)quipment, (P)otions, (C)artographer, (T)emple, (D)ungeon"
msg = "Town Center: There are a number of shops where you can buy supplies for your adventure. The catacomb " \
          "entrance is carved into the side of the mountain nearby. "
image = images.small_village


# Function to navigate the town
def enter(our_hero):
    print("town.enter")
    router.current_controller = sys.modules[__name__]
    # Save our hero every time he/she enters the town.  This will capture coming back from the weapons shop,
    # the temple, or the dungeon.  This means a hero in the dungeon that doesn't come back doesn't get updated.

    return screen.paint(
        hero=our_hero,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=view.screen.list_inventory(our_hero),
        sound=None,
        sleep=250
    )


def process(our_hero, action):
    print("town.process: " + action)
    # Visit the Shop to buy stuff
    if action.lower() == "e":
        return equipment_shop.enter(our_hero)

    # Go into the Map Shop
    if action.lower() == "c":
        return cartography_shop.enter(our_hero)

    # Visit the Magic shop
    if action.lower() == "p":
        return enchantment_shop.enter(our_hero)

    # Go into the Temple
    if action.lower() == "t":
        return temple.enter(our_hero)

    # Enter Dungeon
    if action.lower() == "d":
        return dungeon.enter(our_hero)

    # Print the Town Page if we don't know what the action is.
    return enter(our_hero)
