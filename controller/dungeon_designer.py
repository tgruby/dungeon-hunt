# The word "controller" in programming often is used to refer to parts of the program that control the flow of
# interactions between the user and the computer.  This is where we will put all of our controller code.
import sys
from view import screen, images
from controller import dungeon_design_router


# This Function is to walk through the dungeon and display the results of moving through the dungeon on the screen. This
# continues to loop until we leave the dungeon.
def enter():
    print("dungeon_designer.enter")
    dungeon_design_router.current_controller = sys.modules[__name__]

    return screen.paint(
        "Modify a Map by First Selecting the Map",
        "Specify a Dungeon Map number between 0 - 4:",
        "...",
        images.dungeon_designer_key,
        "Select a Map"
    )


def process(dungeon, action):
    print("dungeon_designer.process: " + action)

    # Select a dungeon
    if action.isdigit():
        return select_a_level(dungeon, action)

    # If the command is nonsense, just repeat current screen.
    return screen.paint(
        "Modify a Map by First Selecting the Map",
        "Specify a Dungeon Map number between 0 - 4:",
        "...",
        images.dungeon_designer_key,
        "Select a Map"
    )


# spawn a monster and go to battle!
def select_a_level(dungeon, action):
    number_picked: int = int(action)
    map = "No Map Selected"
    message = "You must select a number between 0 - 4!"
    if len(dungeon.levels) > number_picked >= 0:
        message = "You have selected map " + str(number_picked) + "."
        map = dungeon.levels[number_picked]["map"]
    return screen.paint(
        "Modify the Dungeon Map",
        "Specify a Dungeon Map number between 0 - 4:",
        message,
        images.dungeon_designer_key,
        map
    )


