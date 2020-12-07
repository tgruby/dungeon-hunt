import db
from view import screen, images
from model import characters


def start_game(gamer_tag, game_token):
    print("intro.start_game")
    # Create game token, the hero, and dungeon to start the game.  Then
    # set the controller to the town.
    print("creating game token and saving character!!!")
    hero = characters.Character(game_token, gamer_tag, characters.warrior)
    db.save_hero(game_token, hero)
    return background()


def background():
    return screen.intro_paint(
        images.title_1,
        "The town of Thordon renowned catacombs have been laid waste by a treacherous red dragon.  The catacombs "
        "had served as a place for both the town dead as well as their treasured secrets from the days of old where "
        "dwarf gold flowed out of the mountain. As the dragon has made it's home in the catacombs, it has slowly "
        "filled with wild animals and more evil things.  Recently, monsters have been leaving the dungeon at night "
        "to drag away town people.  The town is desperate for someone to save them from this deadly decline.  Will you "
        "be their hero?",
        None,
        'Press any key...',
        None,
        None
    )