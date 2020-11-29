import db
import sys
import random
from view import screen, images
from controller import router, dungeon, init_game


# This function controls fighting with a monster
def enter(our_hero):
    print("dungeon_fight.enter")
    router.current_controller = sys.modules[__name__]

    return default_screen(our_hero)


# This Function is to attack the monster. This includes the loop to continue to attack until someone dies, or our hero
# runs away.
def process(our_hero, action):
    message = ""
    if action.lower() == "f":
        message = our_hero.attack_the_monster()
        if our_hero.monster.is_alive():
            message = message + '\n ' + our_hero.monster.attack(our_hero)
            if not our_hero.is_alive():
                return hero_is_slain(our_hero)
            return screen.paint(
                our_hero,
                "(F)ight, (R)un away!",
                message,
                our_hero.view.generate_perspective(),
                our_hero.monster.image,
                None
            )
        else:
            # Monster has been killed
            our_hero.view.dungeon.complete_challenge(our_hero)
            if our_hero.monster.name == "Red Dragon":
                return dragon_killed(our_hero)
            # Grab Gold
            our_hero.gold += our_hero.monster.gold
            # Check to see if the monster drops it's weapon. If so, put it in the hero's inventory.
            drop_weapon = random.randint(0, 3)
            if drop_weapon == 0:
                our_hero.inventory.append(our_hero.monster.weapon)
                message = message + " The monster has dropped " + our_hero.monster.weapon["name"] + "!"
            message = message + " Digging through the %s remains you found %d gold!" % (our_hero.monster.name, our_hero.monster.gold)
            commands = "Press Enter to continue..."
            our_hero.monster = None

            router.current_controller = dungeon
            return screen.paint(
                our_hero,
                commands,
                message,
                our_hero.view.generate_perspective(),
                images.treasure_chest,
                None
            )

    # Run Away
    if action.lower() == "r":
        # The monster gets one last parting shot as you flee.
        message = our_hero.monster.attack(our_hero)
        if not our_hero.is_alive():
            return hero_is_slain(our_hero)

        message += '\n ' + "You run as fast as your little legs will carry you and get away..."
        our_hero.monster = None

        return screen.paint(
            our_hero,
            "(F)ight, (R)un away!",
            message,
            our_hero.view.generate_perspective(),
            "You got away!",
            None
        )

    return default_screen(our_hero)


# routine to run if your hero is slain
def hero_is_slain(our_hero):
    router.current_controller = init_game
    # End the Game, save the character to the leaderboard (if they are good enough).
    lb = db.load_leaderboard()
    lb.add_leader(our_hero)
    db.save_leaderboard(lb)
    # Delete our Hero file so we have to create a new hero
    db.delete_hero(our_hero.game_token)
    our_hero.game_token = None

    return screen.paint(
        our_hero,
        "press Spacebar to start a new game",
        "You have been slain!",
        our_hero.view.generate_perspective(),
        images.death,
        None
    )


# routine to run if your hero kills the dragon
def dragon_killed(our_hero):
    return images.castle + "You have slain the dragon!!! " \
                           "The village rejoices, the dungeons slowly empty of monsters and return \n" \
                           "to the profitable gold mines they once were.  You are made king over all the " \
                           "local lands and reign for \n" \
                           "many peaceful years.  Congratulations!!!"


def default_screen(our_hero):
    return screen.paint(
        our_hero,
        "(F)ight, (R)un away!",
        "A " + our_hero.monster.name + " stands before you, blocking your path!",
        our_hero.view.generate_perspective(),
        our_hero.monster.image,
        None
    )