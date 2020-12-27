import random
from view import images


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
        damage = random.randint(0, self.hit_points)
        damage += 10 * level  # make it harder as you go.
        # Calculate Damage prevented by protection
        protection = 0
        if character.equipped_armor is not None:
            protection += random.randint(4, -character.equipped_armor["damage"])
        if character.equipped_shield is not None:
            protection += random.randint(4, -character.equipped_shield["damage"])
        damage = damage - protection
        # Prevent damage from being negative (healing the hero)
        if damage < 0:
            damage = 0
        # Subtract the damage from our hero's hit points
        character.hit_points -= damage
        return 'You triggered a trap in the room! A %s swings down from the ceiling smashing into you dealing ' \
               '%d damage!' % (self.name, damage)


# This Function is to decide which trap to spawn in a given dungeon level.
def get_a_trap_for_dungeon_level(level_id):
    return Trap(mace_trap)


# Dictionaries of all Traps in the Game

mace_trap = {
    "name": "Morning Star",
    "type": "trap",
    "level": 5,
    "image": images.mace,
    "max_hit_points": 20
}

all_traps = [
    mace_trap
]
