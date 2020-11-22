import os
import pickle
from model import characters, dungeon, dungeon_creator


# This function saves our hero as he/she exists right now.
def save_hero(our_hero):
    save('our_hero', our_hero)


# This helper function is to save our hero to a "pickle" file, python's standard way to save objects to a file.
def load_hero():
    hero = load('our_hero')
    if hero is None:
        # We failed to load the hero from the file.  In this case, just create a new hero.
        hero = characters.Character(characters.warrior)
        hero.name = "Our Hero"
    return hero


# This function will be called when our hero is killed.  That means you can't play him/her again after death!
def delete_hero():
    delete("our_hero")


# This helper function is to open dungeons to a "pickle" file, python's standard way to save objects to a file.
def load_dungeon():
    d = load('dungeon')
    if d is None:
        # We failed to load from the file. In this case, just create new dungeons.
        d = dungeon.Dungeon(dungeon_creator.generate_dungeon_levels())
        save_dungeon(d)
    return d


# This function saves our dungeons as it exists right now.
def save_dungeon(d):
    save('dungeon', d)


# This function will be called when our hero is killed.  That means you can't play the same dungeons again after death!
def delete_dungeon():
    delete("dungeon")


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
            # Load object from the file (instead of creating a new one.
            my_object = pickle.load(load_file)
            # After the object is read from file, return it
            return my_object
    except IOError:
        return None


# This function will be called when our hero is killed.  That means you can't play him/her again after death!
def delete(name):
    os.remove(name + '.pkl')
