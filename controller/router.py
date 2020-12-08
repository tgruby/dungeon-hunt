import db
from controller import town

current_controller = town


# Next Step gets called by the webserver and supplies the action by the user. It will call the
# sub-controller and pass in the action.
def process(token, action):
    # print("Router:")
    # print("   Controller..." + current_controller.__name__)
    # print("   Token........" + token)
    # print("   Action......." + str(action))

    # Load our hero into memory.
    our_hero = db.load_hero(token)
    if our_hero is None:
        return None

    if action is None:
        updated_screen = current_controller.enter(our_hero)
    else:
        updated_screen = current_controller.process(our_hero, action)
    # After every move is processed, save the state of our hero.
    if our_hero.game_token is not None:
        db.save_hero(token, our_hero)

    if updated_screen is None:
        # set update_screen to an error message if blank response
        assert isinstance(token, object)
        updated_screen = ["Error Processing Controller:",
                          "  controller..." + current_controller.__name__,
                          "  action......." + action,
                          "  token........" + str(token)]

    return updated_screen
