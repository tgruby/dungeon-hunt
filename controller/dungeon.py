# The word "controller" in programming often is used to refer to parts of the program that control the flow of
# interactions between the user and the computer.  This is where we will put all of our controller code.
import random

from model import items, monsters, traps, maps
from view import screen, images
from controller import dungeon_inventory, dungeon_fight, town

commands = "Left (A), Right (D), Forward (W), (I)nventory"
message = "You crawl into the dark cave at the side of the mountain and enter the Catacombs!"


def paint(our_hero, msg, sound):
    return screen.paint_two_panes(
        hero=our_hero,
        commands=commands,
        messages=msg,
        left_pane_content=our_hero.view.generate_perspective(),
        right_pane_content=show_map(our_hero),
        sound=sound,
        delay=0,
        interaction_type='key_press'
    )


# This Function is to walk through the dungeon and display the results of moving through the dungeon on the screen. This
# continues to loop until we leave the dungeon.
def process(game, action):
    our_hero = game.character

    if action is None:
        return paint(our_hero, message, None)

    # Turn Left
    if action.lower() == "a":
        msg = our_hero.view.turn_left()
        return paint(our_hero, msg, None)

    # Turn Right
    if action.lower() == "d":
        msg = our_hero.view.turn_right()
        return paint(our_hero, msg, None)

    # Step Forward
    if action.lower() == "w":
        msg = our_hero.view.step_forward()

        if our_hero.view.current_level_id < 0:
            # we have left the dungeon_0, return
            our_hero.view.set_starting_position()
            game.current_controller = 'town'
            return town.process(game, None)

        if msg != "You can't walk through walls!":
            our_hero.step_count += 1
            if our_hero.clairvoyance_count > 0:
                our_hero.clairvoyance_count -= 1  # Subtract the count for every step.

        sound = None
        if msg == "You climb down into the next dungeon!":
            sound = 'open-door'
        elif msg == "This door is locked.":
            sound = 'footstep'

        stepped_on = our_hero.view.get_position_info()
        # Check to see if we have met the Dragon
        if stepped_on == our_hero.view.x_marks_the_spot:
            print("You encounter the Dragon!")
            our_hero.monster = monsters.Monster(monsters.red_dragon)
            game.current_controller = 'dungeon_fight'
            return dungeon_fight.process(game, None)

        # Check to see if we have stepped on Treasure
        if stepped_on == our_hero.view.treasure:
            print("Hero finds Treasure!")
            return found_treasure(game)

        # Check to see if we have stepped onto a Trap
        if stepped_on == our_hero.view.trap:
            print("Hero steps on a Trap!")
            return stepped_on_trap(game)

        # Check to see if we have ran into a Monster
        if stepped_on == our_hero.view.monstr:
            print("Hero runs into a Monster!")
            return fight_monster(game)

        return paint(our_hero, msg, sound)

    # Look in backpack at the hero's inventory
    if action.lower() == "i":
        game.current_controller = 'dungeon_inventory'
        return dungeon_inventory.process(game, None)

    # If the command is nonsense, just repeat current screen.
    return paint(our_hero, ' ', None)


# spawn a monster and go to battle!
def fight_monster(game):
    our_hero = game.character
    if not our_hero.view.dungeon.is_challenge_completed(our_hero):
        monster = monsters.get_a_monster_for_dungeon_level(our_hero.view.current_level_id)
        our_hero.monster = monster
        game.current_controller = 'dungeon_fight'
        return dungeon_fight.process(game, None)
    # else we have already fought this monster...
    return paint(our_hero, "You see a body crumpled against the wall...", None)


# Show the map if our hero has a map for this dungeon
def show_map(our_hero):
    # First check to see if we have the map.
    for i in our_hero.inventory:
        if "number" in i:
            if i["type"] == "map" and i["number"] == our_hero.view.current_level_id:
                return our_hero.view.current_level_map

    # Otherwise, see if we have drank the potion.
    if our_hero.clairvoyance_count > 0:
        return our_hero.view.current_level_map
    else:
        return "Its dark down here\n    on level " + str(our_hero.view.current_level_id)


# This function is called back from the physics module when the character steps on a treasure chest.
def found_treasure(game):
    our_hero = game.character

    if not our_hero.view.dungeon.is_challenge_completed(our_hero):
        our_hero.view.dungeon.complete_challenge(our_hero, 'treasure')
        # Save picked_up_treasure to a pkl file so doesn't reset after a restart.
        max_gold = (our_hero.view.current_level_id + 2) * 15
        min_gold = (our_hero.view.current_level_id + 1) * 5
        treasure = random.randint(min_gold, max_gold)
        our_hero.gold += treasure
        game.score += 10  # Obtain 10 points per treasure
        msg: str = " You found a treasure chest with %d gold in it!" % treasure
        # Check to see if there is a magic item in the treasure chest. If so, put it in the hero's inventory.
        drop_weapon = random.randint(0, 19)  # 5%
        if drop_weapon == 0:
            weapon = items.magical_items[random.randint(0, len(items.magical_items) - 1)]
            our_hero.inventory.append(weapon)
            msg += " You find a %s in the chest!" % weapon["name"]
        # Check to see if the chest contains a map.
        drop_map = random.randint(0, 5)  # 20%
        if drop_map == 0:
            #  Drop the current dungeon level map.  If they have it, don't drop.
            m = maps.map_list[our_hero.view.current_level_id]
            if m not in our_hero.inventory:
                our_hero.inventory.append(m)
                msg += " You find a map in the chest!"
        # Check to see if we have completed all the challenges.  If so, drop a skeleton key.
        if our_hero.view.dungeon.is_all_challenges_complete(our_hero.view.current_level_id):
            our_hero.inventory.append(items.skeleton_key)
            msg += " You find a %s!" % items.skeleton_key["name"]

        cmd = "Press any key to continue..."
        return screen.paint_two_panes(
            hero=our_hero,
            commands=cmd,
            messages=msg,
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=images.treasure_chest,
            sound='challenge-complete',
            delay=500,
            interaction_type='key_press'
        )
    # else you have already picked up this chest
    return paint(our_hero, "You see an empty treasure chest...", None)


def stepped_on_trap(game):
    our_hero = game.character
    if not our_hero.view.dungeon.is_challenge_completed(our_hero):
        our_hero.view.dungeon.complete_challenge(our_hero, 'trap')
        trap = traps.get_a_trap_for_dungeon_level(our_hero.view.current_level_id)
        msg = trap.triggered(our_hero)

        if not our_hero.is_alive():
            # Hero has been killed
            game.game_over = True
            game.killed_by = 'Trap, L' + str(our_hero.view.current_level_id)
            return screen.paint_two_panes(
                hero=our_hero,
                commands='Enter your name for the leaderboard...',
                messages=msg + " You have been killed!",
                left_pane_content=images.tombstone,
                right_pane_content=trap.image,
                sound='death-durg',
                delay=1000,
                interaction_type='enter_press'
            )

        # return the damage summary you took from the trap
        return screen.paint_two_panes(
            hero=our_hero,
            commands=commands,
            messages=msg,
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=trap.image,
            sound='morning-star-trap',
            delay=500,
            interaction_type='key_press'
        )
    else:
        return paint(our_hero, "A morning star is hanging from the ceiling...", None)
