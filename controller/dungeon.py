# The word "controller" in programming often is used to refer to parts of the program that control the flow of
# interactions between the user and the computer.  This is where we will put all of our controller code.
import random

from model import items, monsters, traps
from view import screen, images
from controller import dungeon_inventory, dungeon_fight, town

commands = "Left (A), Right (D), Forward (W), (I)nventory"
message = "You crawl into the dark cave at the side of the mountain and enter the Dungeon!"


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

        # Step forward
        return paint(our_hero, msg, 'footstep')

    # Look in backpack at the hero's inventory
    if action.lower() == "i":
        game.current_controller = 'dungeon_inventory'
        return dungeon_inventory.process(game, None)

    # If the command is nonsense, just repeat current screen.
    return paint(our_hero, "Huh?", None)


# spawn a monster and go to battle!
def fight_monster(game):
    our_hero = game.character
    if not our_hero.view.dungeon.is_challenge_completed(our_hero):
        our_hero.view.dungeon.complete_challenge(our_hero)
        monster = monsters.get_a_monster_for_dungeon(our_hero.view.current_level_id)
        our_hero.monster = monster
        game.current_controller = 'dungeon_fight'
        return dungeon_fight.process(game, None)
    # else we have already fought this monster...
    return paint(our_hero, "You see a monster's body crumpled against the wall...", None)


# Show the map if our hero has a map for this dungeon
def show_map(our_hero):
    dungeon_id = our_hero.view.current_level_id
    for i in our_hero.inventory:
        if "number" in i:
            if i["number"] == dungeon_id and i["type"] == "map":
                return our_hero.view.current_level_map
    return "You have no map for Level " + str(our_hero.view.current_level_id)


# This function is called back from the physics module when the character steps on a treasure chest.
def found_treasure(game):
    our_hero = game.character

    if not our_hero.view.dungeon.is_challenge_completed(our_hero):
        our_hero.view.dungeon.complete_challenge(our_hero)
        # Save picked_up_treasure to a pkl file so doesn't reset after a restart.
        max_gold = (our_hero.view.current_level_id + 2) * 30
        min_gold = (our_hero.view.current_level_id + 1) * 30
        treasure = random.randint(min_gold, max_gold)
        our_hero.gold += treasure
        game.score += 10  # Obtain 10 points per treasure
        msg: str = " You have found a treasure chest with %d gold in it!" % treasure
        # Check to see if there is a weapon in the treasure chest. If so, put it in the hero's inventory.
        drop_weapon = random.randint(0, 5)  # 17%
        if drop_weapon == 0:
            weapon = items.equipment_list[random.randint(0, len(items.equipment_list) - 1)]
            our_hero.inventory.append(weapon)
            msg += " You find a %s in the chest!" % weapon["name"]
        cmd = "Press any key to continue..."
        return screen.paint_two_panes(
            hero=our_hero,
            commands=cmd,
            messages=msg,
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=images.treasure_chest,
            sound=None,
            delay=500,
            interaction_type='key_press'
        )
    # else you have already picked up this chest
    return paint(our_hero, "You see an empty treasure chest...", None)


def stepped_on_trap(game):
    our_hero = game.character
    if not our_hero.view.dungeon.is_challenge_completed(our_hero):
        our_hero.view.dungeon.complete_challenge(our_hero)
        trap = traps.get_a_trap_for_dungeon_level(our_hero.view.current_level_id)

        if not our_hero.is_alive():
            # Hero has been killed
            game.game_over = True
            return screen.paint_two_panes(
                hero=our_hero,
                commands='Press any key...',
                messages=trap.triggered(our_hero) + " You have been killed!",
                left_pane_content=images.tombstone_2,
                right_pane_content=trap.image,
                sound=None,
                delay=1000,
                interaction_type='key_press'
            )

        # return the damage summary you took from the trap
        return screen.paint_two_panes(
            hero=our_hero,
            commands=commands,
            messages=trap.triggered(our_hero),
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=trap.image,
            sound=None,
            delay=500,
            interaction_type='key_press'
        )
    else:
        return paint(our_hero, "You see a morning star hanging from the ceiling...", None)
