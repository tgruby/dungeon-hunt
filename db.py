import os
import pickle
from model import leaderboard, games


def init_db():
    try:
        os.mkdir('data')
    except OSError as error:
        # supressed due to this is the normal operation. TODO: fix this so we check first before trying to make.
        pass


def load_leaderboard():
    lb = load('data/leaderboard')
    if lb is None:
        lb = leaderboard.Leaderboard([])
    return lb


def save_leaderboard(leader_board):
    save('data/leaderboard', leader_board)


def load_game(game_id):
    return load('data/game_' + game_id)


# This function saves our hero as he/she exists right now.
def save_game(game_id, game_object):
    save('data/game_' + game_id, game_object)


# This function will be called when our hero is killed.  That means you can't play him/her again after death!
def delete_game(game_id):
    delete('data/game_' + game_id)


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
        print("Can't find file: " + name)
        return None


# This function will be called when the hero is killed.  That means you can't play him/her again after death!
def delete(name):
    try:
        os.remove(name + '.pkl')
    except OSError as error:
        print("Unable to Delete File: " + name)
        pass  # Don't stop the game if we can't delete the file.
