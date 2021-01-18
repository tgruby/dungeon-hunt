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
    def triggered(self, character):
        #  Calculate Damage Inflicted... changing this to be 20% of the character's HP.
        damage = round(character.max_hit_points * 0.2)
        character.hit_points -= damage
        return 'You triggered a trap in the room! A %s swings down from the ceiling smashing into you dealing ' \
               '%d damage!' % (self.name, damage)


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
