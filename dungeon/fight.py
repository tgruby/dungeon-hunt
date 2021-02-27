import random
from town import items
from game_play import images, screen, level_complete


# This Function is to attack the monster. This includes the loop to continue to attack until someone dies, or our hero
# runs away.
def process(game, action):
    hero = game.character
    dungeon = game.dungeon
    monster = dungeon.current_monster

    if action is None:
        return paint(game, monster.image, "A " + monster.name + "stands before you, blocking your path!")

    if action.lower() == "f":
        message = hero.attack_monster(monster)
        if monster.is_alive():
            message = message + '\n ' + monster.attack(hero)
            if not hero.is_alive():
                return hero_is_slain(game, message)
            return paint(game, monster.image, message)
        else:
            # Monster has been killed
            dungeon.complete_challenge(hero.view.current_x, hero.view.current_y, 'monster')
            # Grab Gold
            hero.gold += monster.gold
            game.increment_monster_score()

            # Check to see if the monster drops it's monster parts. If so, put it in the hero's inventory.
            # Have monsters drop less the deeper the hero goes into the dungeon.
            drop_part = random.randint(0, game.dungeon.current_level_id)
            if drop_part == 0:
                hero.monster_parts += 1
                message = message + ' You recover %s from the %s!' % (monster.item_dropped["name"], monster.name)
            message = message + ' Digging through the %s remains you found %d gold!' % (monster.name, monster.gold)
            commands = "Press any key to continue..."

            if monster.is_boss:
                dungeon.current_monster = None
                return level_complete.process(game, True, monster)

            game.dungeon.current_monster = None
            game.current_controller = 'dungeon'
            return screen.paint_two_panes(
                game=game,
                commands=commands,
                messages=message,
                left_pane_content=hero.view.generate_perspective(),
                right_pane_content=images.treasure_chest,
                sound='challenge-complete',
                delay=500,
                interaction_type='key_press'
            )

    # Run Away
    if action.lower() == "r":
        # The monster gets one last parting shot as you flee.
        message = monster.attack(hero)
        if not hero.is_alive():
            return hero_is_slain(game)

        message += '\n ' + "You run as fast as your little legs will carry you and... Get away!"
        hero.monster = None
        #  Turn around and go one step back.
        hero.view.turn_right()
        hero.view.turn_right()
        hero.view.step_forward()
        game.current_controller = 'dungeon'
        return paint(game, "You've Escaped!", message)

    # Default message if they typed jibberish
    return paint(game, monster.image, "A " + monster.name + " stands before you, blocking your path!")


# routine if your hero is slain
def hero_is_slain(game, message):
    monster = game.dungeon.current_monster
    hero = game.character
    if items.lucky_rock in hero.inventory:
        # The lucky rock saves the character from dying!
        msg = "   You are struck down by the " + monster.name + "!" \
              "\nAs you lay dying, " \
              "\nyour L U C K Y  R O C K begins to glow...\n" \
              "your strength returns and\n" \
              "you scramble away from the monster.\n" \
              "The rock crumbles into dust!"
        game.dungeon.current_monster = None
        hero.hit_points = hero.max_hit_points / 2
        hero.inventory.remove(items.lucky_rock)
        #  Turn around and crawl one step back.
        hero.view.turn_right()
        hero.view.turn_right()
        hero.view.step_forward()
        game.current_controller = 'dungeon'

        return screen.paint_two_panes(
            game=game,
            commands='Press any key to continue...',
            messages='Your still Alive!',
            left_pane_content=images.lucky_rock_glow,
            right_pane_content=msg,
            sound='magic',
            delay=2000,
            interaction_type='key_press'
        )
    else:
        game.game_over = True
        game.status = 'KIA: ' + game.dungeon.current_monster.name + ', L' + str(game.dungeon.current_level_id)

        return screen.paint_two_panes(
            game=game,
            commands='Press the Enter key to continue...',
            messages=message + " You have been slain! Your game score is " + str(game.score) + ". Better luck next time...",
            left_pane_content=images.tombstone,
            right_pane_content=game.dungeon.current_monster.image,
            sound='death-dirge',
            delay=2000,
            interaction_type='key-press'
        )


def paint(game, image, msg):
    return screen.paint_two_panes(
        game=game,
        commands="(F)ight, (R)un away!",
        messages=msg,
        left_pane_content=game.character.view.generate_perspective(),
        right_pane_content=image,
        sound=None,
        delay=0,
        interaction_type='key_press'
    )
