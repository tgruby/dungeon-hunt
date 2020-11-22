from controller import dungeon_designer
import db

current_controller = dungeon_designer


# Next Step gets called by the webserver and supplies the action by the user. It will call the
# sub-controller and pass in the action.
def process(action):
    print("design_router.current_controller: " + current_controller.__name__)

    # Load the dungeon into memory.
    dungeon = db.load_dungeon()
    if action is None:
        updated_screen = current_controller.enter(dungeon)
    else:
        updated_screen = current_controller.process(dungeon, action)
    # After every move is processed, save the state of our hero.
    db.save_dungeon(dungeon)

    if updated_screen is None:
        # set update_screen to an error message if blank response
        updated_screen = ["Error Processing Controller " + current_controller.__name__, "Press any key to continue..."]

    return updated_screen
