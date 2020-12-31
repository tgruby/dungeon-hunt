import textwrap
from game_play import images, screen
import town

commands = "(L)eave"
image = images.small_village
help_content = "Dungeon of Thordon is a maze strategy game, requiring you to solve each maze, while not being killed by monsters or traps. " \
               " You will need to find skeleton keys to unlock the next maze (found behind doors). " \
               "Gold and sometimes maps and magical items can be found in chests. " \
               "although be careful opening doors, sometimes there are traps instead. Monsters are there to block your path, " \
               "chose to fight or run away, but they too can give you goodies if you kill them. " \
               "Gear up in town with armor, weapons, and magical potions.\n\nGood " \
               "luck, young warrior! "


def process(game, action):

    if action is None:
        return paint(game.character)

    # Visit the Shop to buy stuff
    if action.lower() == "l":
        game.current_controller = 'town'
        return town.process(game, None)

    # Something else?
    return paint(game.character)


def paint(hero):
    # Print the Town Page if we don't know what the action is.
    # Wrap long of narratives
    wrapper = textwrap.TextWrapper(width=46)
    word_list = wrapper.wrap(text=help_content)
    # Print each line
    formatted_content = ""
    for line in word_list:
        formatted_content += line + '\n'

    return screen.paint_two_panes(
        hero=hero,
        commands=commands,
        messages=None,
        left_pane_content=image,
        right_pane_content=formatted_content,
        sound=None,
        delay=0,
        interaction_type='key_press'
    )
