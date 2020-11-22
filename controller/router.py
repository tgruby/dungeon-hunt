from controller import town
import db

current_controller = town


# Next Step gets called by the webserver and supplies the action by the user. It will call the
# sub-controller and pass in the action.
def process(action):
    print("router.current_controller: " + current_controller.__name__)

    # Load our hero into memory.
    our_hero = db.load_hero()
    if action is None:
        updated_screen = current_controller.enter(our_hero)
    else:
        updated_screen = current_controller.process(our_hero, action)
    # After every move is processed, save the state of our hero.
    db.save_hero(our_hero)

    if updated_screen is None:
        # set update_screen to an error message if blank response
        updated_screen = ["Error Processing Controller " + current_controller.__name__, "Press any key to continue..."]

    return updated_screen
