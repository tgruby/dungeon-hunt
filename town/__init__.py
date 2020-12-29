import game_play.screen
from game_play import images, screen
import dungeon
from town import cartography_shop, equipment_shop, help, potion_shop, temple

commands = "(E)quipment Shop, (P)otion Shop, (M)ap Shop, (T)emple, (D)ungeon, (H)elp"
msg = "Thordon Town Center: There are a number of shops where you can buy supplies for your adventure. The catacomb " \
      "entrance is carved into the side of the mountain nearby. "
image = images.small_village


def process(game, action):
    if action is None:
        return paint(game.character)

    # Visit the Shop to buy stuff
    if action.lower() == "e":
        game.current_controller = 'town.equipment_shop'
        return equipment_shop.process(game, None)

    # Go into the Map Shop
    if action.lower() == "m":
        game.current_controller = 'town.cartography_shop'
        return cartography_shop.process(game, None)

    # Visit the Magic shop
    if action.lower() == "p":
        game.current_controller = 'town.potion_shop'
        return potion_shop.process(game, None)

    # Go into the Temple
    if action.lower() == "t":
        game.current_controller = 'town.temple'
        return temple.process(game, None)

    # Enter Dungeon
    if action.lower() == "d":
        game.current_controller = 'dungeon'
        return dungeon.process(game, 'enter')

    # Enter Dungeon
    if action.lower() == "h":
        game.current_controller = 'town.help'
        return help.process(game, None)

    # Cheat to help with testing.... yank after testing
    if action.lower() == "$":
        game.character.gold = 500

    # Something else?
    return paint(game.character)


def paint(hero):
    # Print the Town Page if we don't know what the action is.
    return screen.paint_two_panes(
        hero=hero,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=game_play.screen.list_inventory(hero),
        sound=None,
        delay=0,
        interaction_type='key_press'
    )
