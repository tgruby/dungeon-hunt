import textwrap
from view import screen, images
from controller import town

commands = "E(x)it"
image = images.small_village
help_content = "Dungeon of Thordon is maze strategy game requiring you to navigate \
mazes, fight monsters, and ultimately defeating the dragon in the last maze. \
For each level, you must find the key to unlock the next level. Your score will \
increase with each monster you kill and each treasure you find. Be on the lookout for magical items \
you can find on the way!  As your hero vanquishes monsters she will level up giving you additional \
health. Make use of the maps, weapons, armor, and potions, and its a good idea to stock up \
before going down to the next level. Each maze gets progressively bigger as \
well, so maps becomes more important the further you go.    Good luck! "


def process(game, action):

    if action is None:
        return paint(game.character)

    # Visit the Shop to buy stuff
    if action.lower() == "x":
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
        interaction_type='enter_press'
    )
