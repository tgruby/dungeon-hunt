import os
import pickle
from model import leaderboard


def init_db():
    try:
        os.mkdir('data')
    except OSError as error:
        print(error)


# This function saves our hero as he/she exists right now.
def save_hero(game_token, hero):
    save('data/game_' + game_token, hero)
    print("Saved Game: " + game_token)


# This helper function is to save our hero to a "pickle" file, python's standard way to save objects to a file.
def load_hero(game_token):
    return load('data/game_' + game_token)


# This function will be called when our hero is killed.  That means you can't play him/her again after death!
def delete_hero(game_token):
    delete('data/game_' + game_token)


# This function saves our hero as he/she exists right now.
def save_leaderboard(leader_board):
    save('data/leaderboard', leader_board)


def load_leaderboard():
    lb = load('data/leaderboard')
    if lb is None:
        lb = leaderboard.Leaderboard()
    return lb


# This function saves our hero as he/she exists right now.
def save(name, my_object):
    # Open the file
    with open(name + '.pkl', 'wb') as save_file:
        # dump our_hero structure into the pickle file
        pickle.dump(my_object, save_file)


# This helper function is to save an object to a "pickle" file, python's standard way to save objects to a file.
def load(name):
    try:
        # Open a File
        with open(name + '.pkl', 'rb') as load_file:
            # Load object from the file
            my_object = pickle.load(load_file)
            # After the object is read from file, return it
            return my_object
    except IOError:
        return None


# This function will be called when the hero is killed.  That means you can't play him/her again after death!
def delete(name):
    os.remove(name + '.pkl')
