import textwrap
from game_play import images, screen
import town

commands = "E(x)it"
image = images.small_village
help_content = "The labyrinth is a 16 level maze of treasure rooms, often filled with treasure, sometimes found with " \
               "traps. Treasure rooms are found at the end of hallways, behind unlocked doors, but to get to the next " \
               "level, you will need a skeleton key. Keys are hidden in chests (along with maps occasionally), " \
               "so if you haven't found the key for a level, keep looking. After clearing a level, you will return to " \
               "town where you can stock up and heal for your next journey down into the abyss.  Initially, " \
               "consider buying a shield. Even the weakest monster attacks can pierce your clothing. Remember items " \
               "found in the dungeon need to manually be equipped from your inventory.   Chose to fight or run away, " \
               "but killing monsters give you gold and possibly items that can be used to create potions. Good luck, " \
               "young warrior! "


def process(game, action):

    if action is None:
        return paint(game)

    # Visit the Shop to buy stuff
    if action.lower() == "x":
        game.current_controller = 'town'
        return town.process(game, None)

    # Something else?
    return paint(game)


def paint(game):
    # Print the Town Page if we don't know what the action is.
    # Wrap long of narratives
    wrapper = textwrap.TextWrapper(width=46)
    word_list = wrapper.wrap(text=help_content)
    # Print each line
    formatted_content = ""
    for line in word_list:
        formatted_content += line + '\n'

    return screen.paint_two_panes(
        game=game,
        commands=commands,
        messages=None,
        left_pane_content=image,
        right_pane_content=formatted_content,
        sound=None,
        delay=0,
        interaction_type='key_press'
    )
