import db
import uuid
import view.screen
from view import screen, images
from controller import router
from model import characters

game_tokens = []

# Special controller to stay on the current screen until a specific keyboard key is pressed
def enter(screen, next_controller, key_required):
    router.current_controller
    print("pause.enter")

    return screen


def process(action):
    print("init_game.process")
    # Create game token, the hero (with the name supplied in the action), and dungeon to start the game.  Then
    # set the controller to the town.
    game_token = str(uuid.uuid4())
    hero = characters.Character(game_token, "Hero", characters.warrior)
    db.save_hero(game_token, hero)
    return town.enter(hero)


def intro_screen():
    return screen.intro_paint(
        images.title_1,
        "The town of Thordale's renowned catacombs have been laid waste by a treacherous red dragon.  The catacombs "
        "had served as a place for both the town dead, as well as their tresured secrets from the days of where the "
        "dwarfs gold flowed through the mountain. As the dragon has made it's home in the catacombs, it has slowly "
        "filled with wild animals and more evil monsters.  Recently, monsters have been leaving the dungeon at night "
        "to attack town people.  The town is desperate for someone to save them from this deadly decline.  Will you "
        "be their hero?",
        'Press any key to play...',
        None
    )


def draw_leaderboard():
    lb = db.load_leaderboard()
    response = view.screen.medium_border + '\n'
    response += " Name              | Score " + '\n'
    response += view.screen.medium_border + '\n'
    for i in lb.top_ten:
        response += " " + view.screen.back_padding(i.name, 17) + " | " \
                    + str(i.experience_points) + '\n'
    response += view.screen.medium_border + '\n'
    return response
