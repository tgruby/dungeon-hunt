# The word "controller" in programming often is used to refer to parts of the program that control the flow of
# interactions between the user and the computer.  This is where we will put all of our controller code.
import sys
import random

from model import items, monsters, traps
from view import screen, images
from controller import router, dungeon_inventory, dungeon_fight, town

commands = "Left (A), Right (D), Forward (W), (I)nventory"
message = "You crawl into the dark cave at the side of the mountain and enter the Dungeon!"


# This Function is to walk through the dungeon and display the results of moving through the dungeon on the screen. This
# continues to loop until we leave the dungeon.
def enter(our_hero):
    print("dungeon.enter")
    router.current_controller = sys.modules[__name__]

    return screen.paint(
        hero=our_hero,
        commands=commands,
        messages=message,
        left_pane_content=our_hero.view.generate_perspective(),
        right_pane_content=show_map(our_hero),
        sound=None,
        sleep=0
    )


def process(our_hero, action):
    print("dungeon.process: " + action)

    # Turn Left
    if action.lower() == "a":
        msg = our_hero.view.turn_left()
        return screen.paint(
            hero=our_hero,
            commands=commands,
            messages=msg,
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=show_map(our_hero),
            sound=None,
            sleep=0
        )

    # Turn Right
    if action.lower() == "d":
        msg: object = our_hero.view.turn_right()
        return screen.paint(
            hero=our_hero,
            commands=commands,
            messages=msg,
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=show_map(our_hero),
            sound=None,
            sleep=0
        )

    # Step Forward
    if action.lower() == "w":
        msg = our_hero.view.step_forward()

        if our_hero.view.current_level_id < 0:
            # we have left the dungeon_0, return
            our_hero.view.set_starting_position()
            return town.enter(our_hero)

        stepped_on = our_hero.view.get_position_info()
        # Check to see if we have met the Dragon
        if stepped_on == our_hero.view.x_marks_the_spot:
            print("Hero encounters the Dragon!")
            our_hero.monster = monsters.Monster(monsters.red_dragon)
            return dungeon_fight.enter(our_hero)

        # Check to see if we have stepped on Treasure
        if stepped_on == our_hero.view.treasure:
            print("Hero finds Treasure!")
            return found_treasure(our_hero)

        # Check to see if we have stepped onto a Trap
        if stepped_on == our_hero.view.trap:
            print("Hero steps on a Trap!")
            return stepped_on_trap(our_hero)

        # Check to see if we have ran into a Monster
        if stepped_on == our_hero.view.monstr:
            print("Hero runs into a Monster!")
            return fight_monster(our_hero)

        # Step forward
        return screen.paint(
            hero=our_hero,
            commands=commands,
            messages=msg,
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=show_map(our_hero),
            sound='footstep',
            sleep=0
        )

    # Look in backpack at the hero's inventory
    if action.lower() == "i":
        return dungeon_inventory.enter(our_hero)

    # If the command is nonsense, just repeat current screen.
    return screen.paint(
        hero=our_hero,
        commands=commands,
        messages="Huh?",
        left_pane_content=our_hero.view.generate_perspective(),
        right_pane_content=show_map(our_hero),
        sound=None,
        sleep=0
    )


# spawn a monster and go to battle!
def fight_monster(our_hero):
    if not our_hero.view.dungeon.is_challenge_completed(our_hero):
        our_hero.view.dungeon.complete_challenge(our_hero)
        monster = monsters.get_a_monster_for_dungeon(our_hero.view.current_level_id)
        our_hero.monster = monster
        return dungeon_fight.enter(our_hero)
    return screen.paint(
        hero=our_hero,
        commands=commands,
        messages="You see a monster's body crumpled against the wall...",
        left_pane_content=our_hero.view.generate_perspective(),
        right_pane_content=show_map(our_hero),
        sound=None,
        sleep=0
    )


# Show the map if our hero has a map for this dungeon
def show_map(our_hero):
    dungeon_id = our_hero.view.current_level_id
    for i in our_hero.inventory:
        if "number" in i:
            if i["number"] == dungeon_id and i["type"] == "map":
                return our_hero.view.current_level_map
    return "You have no map for Level " + str(our_hero.view.current_level_id)


# This function is called back from the physics module when the character steps on a treasure chest.
def found_treasure(our_hero):

    if not our_hero.view.dungeon.is_challenge_completed(our_hero):
        our_hero.view.dungeon.complete_challenge(our_hero)
        # Save picked_up_treasure to a pkl file so doesn't reset after a restart.
        max_gold = (our_hero.view.current_level_id + 1) * 30
        min_gold = our_hero.view.current_level_id * 30
        treasure = random.randint(min_gold, max_gold)
        our_hero.gold += treasure
        msg: str = " You have found a treasure chest with %d gold in it!" % treasure
        # Check to see if there is a weapon in the treasure chest. If so, put it in the hero's inventory.
        drop_weapon = random.randint(0, 5)  # 17%
        if drop_weapon == 0:
            weapon = items.equipment_list[random.randint(0, len(items.equipment_list) - 1)]
            our_hero.inventory.append(weapon)
            msg += " You find a %s in the chest!" % weapon["name"]
        cmd = "Press any key to continue..."
        return screen.paint(
            hero=our_hero,
            commands=cmd,
            messages=msg,
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=images.treasure_chest,
            sound=None,
            sleep=00
        )
    return screen.paint(
        hero=our_hero,
        commands=commands,
        messages="You see an empty treasure chest...",
        left_pane_content=our_hero.view.generate_perspective(),
        right_pane_content=show_map(our_hero),
        sound=None,
        sleep=0
    )


def stepped_on_trap(our_hero):
    if not our_hero.view.dungeon.is_challenge_completed(our_hero):
        our_hero.view.dungeon.complete_challenge(our_hero)
        trap = traps.get_a_trap_for_dungeon_level(our_hero.view.current_level_id)
        # TODO: What if this kills the hero
        return screen.paint(
            hero=our_hero,
            commands=commands,
            messages=trap.triggered(our_hero),
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=trap.image,
            sound=None,
            sleep=00
        )
    else:
        return screen.paint(
            hero=our_hero,
            commands=commands,
            messages="You see a morning star hanging from the ceiling...",
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=show_map(our_hero),
            sound=None,
            sleep=0
        )
