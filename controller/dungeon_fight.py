import random
from model import items
from view import screen, images


# This Function is to attack the monster. This includes the loop to continue to attack until someone dies, or our hero
# runs away.
def process(game, action):
    our_hero = game.character

    if action is None:
        return paint(our_hero, "A " + our_hero.monster.name + " stands before you, blocking your path!")

    if action.lower() == "f":
        message = our_hero.attack_the_monster()
        if our_hero.monster.is_alive():
            message = message + '\n ' + our_hero.monster.attack(our_hero)
            if not our_hero.is_alive():
                return hero_is_slain(game)
            return paint(our_hero, message)
        else:
            # Monster has been killed
            our_hero.view.dungeon.complete_challenge(our_hero, 'monster')
            # Grab Gold
            our_hero.gold += our_hero.monster.gold
            game.score += our_hero.monster.level * 10  # Increase Score for killing monsters.
            # Check to see if the monster drops it's weapon. If so, put it in the hero's inventory.
            drop_weapon = random.randint(0, 3)
            if drop_weapon == 0:
                our_hero.inventory.append(our_hero.monster.weapon)
                message = message + " The monster has dropped " + our_hero.monster.weapon["name"] + "!"
            message = message + " Digging through the %s remains you found %d gold!" % (our_hero.monster.name, our_hero.monster.gold)
            # Check to see if we have completed all the challenges.  If so, drop a skeleton key.
            if our_hero.view.dungeon.is_all_challenges_complete(our_hero.view.current_level_id):
                our_hero.inventory.append(items.skeleton_key)
                message += " You find a %s!" % items.skeleton_key["name"]
            commands = "Press any key to continue..."

            if our_hero.monster.name == "Red Dragon":
                return dragon_killed(our_hero)

            our_hero.monster = None
            game.current_controller = 'dungeon'
            return screen.paint_two_panes(
                hero=our_hero,
                commands=commands,
                messages=message,
                left_pane_content=our_hero.view.generate_perspective(),
                right_pane_content=images.treasure_chest,
                sound=None,
                delay=500,
                interaction_type='key_press'
            )

    # Run Away
    if action.lower() == "r":
        # The monster gets one last parting shot as you flee.
        message = our_hero.monster.attack(our_hero)
        if not our_hero.is_alive():
            return hero_is_slain(game)

        message += '\n ' + "You run as fast as your little legs will carry you and... Get away!"
        our_hero.monster = None
        # TODO: Get the hero lost. Randomly put them somewhere else in the dungeon level with an open space.

        game.current_controller = 'dungeon'
        return paint(our_hero, message)

    # Default message if they typed jibberish
    return paint(our_hero, "A " + our_hero.monster.name + " stands before you, blocking your path!")


# routine to run if your hero is slain
def hero_is_slain(game):
    game.game_over = True
    our_hero = game.character
    game.killed_by = our_hero.monster.name + ', L' + str(our_hero.view.current_level_id)

    return screen.paint_two_panes(
        hero=our_hero,
        commands="Enter your name for the leaderboard...",
        messages="You have been slain! Your game score is " + str(game.score) + ". Better luck next time...",
        left_pane_content=images.tombstone,
        right_pane_content=our_hero.monster.image,
        sound=None,
        delay=1000,
        interaction_type='enter_press'
    )


# TODO: routine to run if your hero kills the dragon
def dragon_killed(game):
    game.game_over = True
    our_hero = game.character
    return screen.paint_two_panes(
        hero=our_hero,
        commands="YOU WON THE GAME!!!",
        messages="You have slain the dragon!!! " \
                 "The village rejoices, the dungeons are emptied of monsters and return \n" \
                 "to the peaceful catacombs.  You are made lord over the " \
                 "local lands and reign for \n" \
                 "many peaceful years.  Congratulations!!!",
        left_pane_content=images.treasure_chest,
        right_pane_content=images.castle,
        sound=None,
        delay=0,
        interaction_type='key_press'
    )


def paint(our_hero, msg):
    return screen.paint_two_panes(
        hero=our_hero,
        commands="(F)ight, (R)un away!",
        messages=msg,
        left_pane_content=our_hero.view.generate_perspective(),
        right_pane_content=our_hero.monster.image,
        sound=None,
        delay=0,
        interaction_type='key_press'
    )
