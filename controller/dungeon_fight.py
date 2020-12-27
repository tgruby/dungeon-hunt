import random
from view import screen, images


# This Function is to attack the monster. This includes the loop to continue to attack until someone dies, or our hero
# runs away.
def process(game, action):
    our_hero = game.character

    if action is None:
        return paint(our_hero, our_hero.monster.image, "A " + our_hero.monster.name + " stands before you, blocking your path!")

    if action.lower() == "f":
        message = our_hero.attack_the_monster()
        if our_hero.monster.is_alive():
            message = message + '\n ' + our_hero.monster.attack(our_hero)
            if not our_hero.is_alive():
                return hero_is_slain(game)
            return paint(our_hero, our_hero.monster.image, message)
        else:
            # Monster has been killed
            our_hero.view.dungeon.complete_challenge(our_hero, 'monster')
            # Grab Gold
            our_hero.gold += our_hero.monster.gold
            game.increment_monster_score(our_hero.monster)

            # Check to see if the monster drops it's weapon. If so, put it in the hero's inventory.
            drop_weapon = random.randint(0, 3)  # 25%
            if drop_weapon == 0:
                our_hero.inventory.append(our_hero.monster.weapon)
                message = message + ' You recover a ' + our_hero.monster.weapon["name"] + " from the monster!"
            message = message + ' Digging through the %s remains you found %d gold!' % (our_hero.monster.name, our_hero.monster.gold)
            commands = "Press any key to continue..."

            if our_hero.monster.name == "Red Dragon":
                return dragon_killed(game)

            our_hero.monster = None
            game.current_controller = 'dungeon'
            return screen.paint_two_panes(
                hero=our_hero,
                commands=commands,
                messages=message,
                left_pane_content=our_hero.view.generate_perspective(),
                right_pane_content=images.treasure_chest,
                sound='challenge-complete',
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
        #  Turn around and go one step back.
        our_hero.view.turn_right()
        our_hero.view.turn_right()
        our_hero.view.step_forward()
        game.current_controller = 'dungeon'
        return paint(our_hero, "You've Escaped!", message)

    # Default message if they typed jibberish
    return paint(our_hero, our_hero.monster.image, "A " + our_hero.monster.name + " stands before you, blocking your path!")


# routine if your hero is slain
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
        sound='death-durg',
        delay=1000,
        interaction_type='enter_press'
    )


# TODO: routine to run if your hero kills the dragon
def dragon_killed(game):
    game.game_over = True
    game.killed_by = 'Winner!'
    our_hero = game.character
    return screen.paint_two_panes(
        hero=our_hero,
        commands="YOU WON THE GAME!!! Enter your name for the leaderboard...",
        messages="You have slain the dragon!!! " \
                 "The village rejoices, the catacombs are emptied of monsters and life returns \n" \
                 "to a peaceful existence. You are made lord over the " \
                 "local lands and reign for \n" \
                 "many peaceful years!!!",
        left_pane_content=images.treasure_chest,
        right_pane_content=images.castle,
        sound='challenge-complete',
        delay=1000,
        interaction_type='enter_press'
    )


def paint(our_hero, image, msg):
    return screen.paint_two_panes(
        hero=our_hero,
        commands="(F)ight, (R)un away!",
        messages=msg,
        left_pane_content=our_hero.view.generate_perspective(),
        right_pane_content=image,
        sound=None,
        delay=0,
        interaction_type='key_press'
    )
