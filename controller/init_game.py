import db
import uuid
from view import screen, images
from controller import town
from model import characters


def show_splash():
    print("init_game.show_splash")
    db.init_db()

    return intro_screen()


def process(action):
    print("init_game.process")
    if action.lower() == 's':
        # Create game token, the hero, and dungeon to start the game.  Then
        # set the controller to the town.
        print("creating game token and saving character!!!")
        game_token = str(uuid.uuid4())
        hero = characters.Character(game_token, "Hero", characters.warrior)
        db.save_hero(game_token, hero)
        return town.enter(hero)
    elif action.lower() == 'l':
        return draw_leaderboard()
    else:
        return intro_screen()


def intro_screen():
    return screen.intro_paint(
        images.title_1,
        "The town of Thordon renowned catacombs have been laid waste by a treacherous red dragon.  The catacombs "
        "had served as a place for both the town dead as well as their treasured secrets from the days of old where "
        "dwarf gold flowed out of the mountain. As the dragon has made it's home in the catacombs, it has slowly "
        "filled with wild animals and more evil things.  Recently, monsters have been leaving the dungeon at night "
        "to drag away town people.  The town is desperate for someone to save them from this deadly decline.  Will you "
        "be their hero?",
        None,
        'Press L to see the Leaderboard, and S to start play...',
        None,
        None
    )


def draw_leaderboard():
    lb = db.load_leaderboard()
    print("LB Count: " + str(len(lb.top_ten)))
    response = "  Rank | Name                       | Score " + '\n'
    response += screen.medium_border + '\n'
    for i in lb.top_ten:
        response += "       | " + screen.back_padding(i.name, 26) + " | " + str(i.experience_points) + '\n'

    return screen.intro_paint(
        images.title_1,
        None,
        response,
        'Press S to start play...',
        None,
        None
    )

