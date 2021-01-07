import random
from game_play import images


# Class object to represent any active monster
class Trap:
    # Class Level Variables

    # Trap Constructor
    def __init__(self, trap_definition):
        self.name = trap_definition["name"]
        self.image = trap_definition["image"]
        self.hit_points = trap_definition["max_hit_points"]
        self.level = trap_definition["level"]

    # Method to call when the trap is triggered
    def triggered(self, character, level):
        #  Calculate Damage Inflicted
        damage = random.randint(0, (self.hit_points + 4 * level))  # make it harder as you go.
        adjusted_damage = character.take_damage(damage)
        return 'You triggered a trap in the room! A %s swings down from the ceiling smashing into you dealing ' \
               '%d damage!' % (self.name, adjusted_damage)


# This Function is to decide which trap to spawn in a given dungeon level.
def get_a_trap_for_dungeon_level(level_id):
    return Trap(mace_trap)


# Dictionaries of all Traps in the Game

mace_trap = {
    "name": "Morning Star",
    "type": "trap",
    "level": 5,
    "image": images.mace,
    "max_hit_points": 10
}

all_traps = [
    mace_trap
]
