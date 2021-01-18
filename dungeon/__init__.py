import town
import random

from dungeon.physics import PointOfView
from town import items
from game_play import images, screen, level_complete
from dungeon import inventory, fight, dungeon_generator, monsters, traps


# Static function for storing completed challenge markers.
def hash_challenge_location(x, y):
    location = str(x) + "-" + str(y)
    return location


class Dungeon:

    def __init__(self):
        self.levels = []
        self.current_level = None
        self.current_level_id = 0
        self.current_monster = None
        self.snake_boss = monsters.Monster(monsters.giant_snake)
        self.cyclops_boss = monsters.Monster(monsters.cyclops)
        self.wraith_boss = monsters.Monster(monsters.wraith)
        self.dragon_boss = monsters.Monster(monsters.red_dragon)

    def generate_next_level(self):
        self.current_level_id += 1
        self.current_level = dungeon_generator.generate_dungeon_level(self.current_level_id)
        self.levels.append(self.current_level)

    def complete_challenge(self, x, y, challenge_type):
        # Mark the location of the challenge as complete so the next time we step here we don't launch a monster or
        # give another treasure
        self.current_level["completed_challenges"].append(hash_challenge_location(x, y))
        # Subtract from the treasure count.  Once all challenges are complete, give user a skeleton key to go to
        # the next level.
        if challenge_type == 'treasure':
            self.current_level['treasures_collected'] += 1
        if challenge_type == 'trap':
            self.current_level['traps_triggered'] += 1
        if challenge_type == 'monster':
            self.current_level['monsters_killed'] += 1

    def is_challenge_completed(self, x, y):
        if hash_challenge_location(x, y) in self.current_level["completed_challenges"]:
            return True
        return False

    def are_all_treasures_collected(self):
        return self.current_level['treasure_count'] - \
               self.current_level['treasures_collected'] == 0

    def is_exit_door_locked(self):
        return self.current_level['exit_door_locked']

    def unlock_exit_door(self):
        self.current_level['exit_door_locked'] = False

    def is_level_completed(self):
        return self.current_level['level_completed']

    def complete_level(self):
        self.current_level['level_completed'] = True

    # This Function is to decide which monster boss to spawn in a given dungeon.
    def get_boss_for_dungeon_level(self):
        # Select a monster appropriate for the level of this dungeon. If this is the first dungeon, just return the rat.
        if self.current_level_id == 5:
            return self.snake_boss
        elif self.current_level_id == 10:
            return self.cyclops_boss
        elif self.current_level_id == 15:
            return self.wraith_boss
        else:
            return self.dragon_boss


commands = "Left (A), Right (D), Forward (W), (I)nventory"
message = "You crawl into the dark cave at the side of the mountain and enter the Catacombs!"


def paint(game, msg, sound):
    return screen.paint_two_panes(
        game=game,
        commands=commands,
        messages=msg,
        left_pane_content=game.character.view.generate_perspective(),
        right_pane_content=show_map(game.character),
        sound=sound,
        delay=0,
        interaction_type='key_press'
    )


# This Function is to walk through the dungeon and display the results of moving through the dungeon on the screen. This
# continues to loop until we leave the dungeon.
def process(game, action):
    hero = game.character

    if action == 'enter':
        if game.dungeon.current_level is None:
            game.dungeon.generate_next_level()
        elif game.dungeon.current_level['level_completed'] is True:
            game.dungeon.generate_next_level()
        hero.view = PointOfView(game)
        return paint(game, message, 'door-slammed')

    if action is None:
        return paint(game, None, None)

    # for testing, give skeleton key
    # if action.lower() == '$':
        # msg = "You stepped on a Skeleton Key!"
        # hero.inventory.append(items.skeleton_key)
        # return paint(game, msg, None)

    # Turn Left
    if action.lower() == "a" or action == "ArrowLeft":
        msg = hero.view.turn_left()
        return paint(game, msg, None)

    # Turn Right
    if action.lower() == "d" or action == "ArrowRight":
        msg = hero.view.turn_right()
        return paint(game, msg, None)

    # Step Forward
    if action.lower() == "w" or action == "ArrowUp":
        msg = hero.view.step_forward()
        sound = None

        if msg == "town":
            # we have left the dungeon, return to town.
            game.current_controller = 'town'
            hero.view = None
            return town.process(game, None)
        elif msg == "level-complete":
            return level_complete.process(game, False, None)
        elif msg == "This door is locked.":
            msg += " You need a skeleton key."
            print("Processing: This door is locked.")
            sound = 'door-locked'
        elif msg != "You can't walk through walls!":
            print("Processing: You can't walk through walls!")
            hero.step_count += 1
            if hero.clairvoyance_count > 0:
                hero.clairvoyance_count -= 1  # Subtract the count for every step.

        stepped_on = hero.view.get_position_info()
        # Check to see if we have met a boss.
        if stepped_on == hero.view.x_marks_the_spot:
            print("hero encounters a Boss!")
            game.dungeon.current_monster = game.dungeon.get_boss_for_dungeon_level()
            game.current_controller = 'dungeon.fight'
            return fight.process(game, None)

        # Check to see if we have stepped on Treasure
        if stepped_on == hero.view.treasure:
            print("Hero finds Treasure!")
            return found_treasure(game)

        # Check to see if we have stepped onto a Trap
        if stepped_on == hero.view.trap:
            print("Hero steps on a Trap!")
            return stepped_on_trap(game)

        # Check to see if we have ran into a Monster
        if stepped_on == hero.view.monstr:
            print("Hero runs into a Monster!")
            return fight_monster(game)

        return paint(game, msg, sound)

    # Look in backpack at the hero's inventory
    if action.lower() == "i":
        game.current_controller = 'dungeon.inventory'
        return inventory.process(game, None)

    # If the command is nonsense, just repeat current screen.
    return paint(game, None, None)


# spawn a monster and go to battle!
def fight_monster(game):
    our_hero = game.character
    if not game.dungeon.is_challenge_completed(our_hero.view.current_x, our_hero.view.current_y):
        game.dungeon.current_monster = monsters.get_a_monster_for_dungeon_level(our_hero.view.current_level_id)
        game.current_controller = 'dungeon.fight'
        return fight.process(game, None)
    # else we have already fought this monster...
    return paint(game, "You see a body crumpled against the wall...", None)


# Show the map if our hero has a map for this dungeon
def show_map(our_hero):
    if our_hero.clairvoyance_count > 0:
        return our_hero.view.current_level_clairvoyance_map
    elif items.dungeon_map in our_hero.inventory:
        return our_hero.view.current_level_map
    else:
        return "        Its dark down here... \n" \
               "Hopefully you are not eaten by a grue."


# This function is called back from the physics module when the character steps on a treasure chest.
def found_treasure(game):
    our_hero = game.character

    if not game.dungeon.is_challenge_completed(our_hero.view.current_x, our_hero.view.current_y):
        game.dungeon.complete_challenge(our_hero.view.current_x, our_hero.view.current_y, 'treasure')
        # Save picked_up_treasure to a pkl file so doesn't reset after a restart.
        level_adjustment = our_hero.view.current_level_id
        if level_adjustment > 5:
            level_adjustment = 5
        max_gold = (level_adjustment + 1) * 10
        min_gold = (level_adjustment + 1) * 1
        treasure = random.randint(min_gold, max_gold)
        our_hero.gold += treasure
        game.increment_treasure_score()
        msg: str = ' You found a treasure chest with %d gold in it!' % treasure

        # Check to see if the chest contains a map.
        drop_map = random.randint(0, 3)  # 25%
        if drop_map == 0:
            #  Drop the current dungeon level map.  If they have it, don't drop.
            if items.dungeon_map not in our_hero.inventory:
                our_hero.inventory.append(items.dungeon_map)
                msg += ' You find a map in the chest!'
        # Check to see if we have completed all the challenges.  If so, drop a skeleton key.
        if our_hero.view.dungeon.are_all_treasures_collected():
            our_hero.inventory.append(items.skeleton_key)
            msg += ' You find a %s!' % items.skeleton_key["name"]

        cmd = "Press any key to continue..."
        return screen.paint_two_panes(
            game=game,
            commands=cmd,
            messages=msg,
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=images.treasure_chest,
            sound='challenge-complete',
            delay=500,
            interaction_type='key_press'
        )
    # else you have already picked up this chest
    return screen.paint_two_panes(
        game=game,
        commands=commands,
        messages="You see an empty treasure chest...",
        left_pane_content=our_hero.view.generate_perspective(),
        right_pane_content=images.empty_treasure_chest,
        sound=None,
        delay=0,
        interaction_type='key_press'
    )


def stepped_on_trap(game):
    our_hero = game.character
    if not our_hero.view.dungeon.is_challenge_completed(our_hero.view.current_x, our_hero.view.current_y):
        our_hero.view.dungeon.complete_challenge(our_hero.view.current_x, our_hero.view.current_y, 'trap')
        trap = traps.Trap(traps.mace_trap)
        msg = trap.triggered(our_hero)

        if not our_hero.is_alive():
            # Hero has been killed
            game.game_over = True
            game.status = 'KIA: Trap, L' + str(our_hero.view.current_level_id)
            return screen.paint_two_panes(
                game=game,
                commands='Press the Enter key to continue...',
                messages=msg + " You have been killed!",
                left_pane_content=images.tombstone,
                right_pane_content=trap.image,
                sound='death-dirge',
                delay=1000,
                interaction_type='key_press'
            )

        # return the damage summary you took from the trap
        return screen.paint_two_panes(
            game=game,
            commands=commands,
            messages=msg,
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=trap.image,
            sound='morning-star-trap',
            delay=500,
            interaction_type='key_press'
        )
    else:
        return screen.paint_two_panes(
            game=game,
            commands=commands,
            messages="A morning star lays in the corner of the room...",
            left_pane_content=our_hero.view.generate_perspective(),
            right_pane_content=images.sprung_trap,
            sound=None,
            delay=None,
            interaction_type='key_press'
        )
