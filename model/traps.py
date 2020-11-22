import random
from view import images
from model import items


# Class object to represent any active monster
class Trap:
    # Class Level Variables

    # Trap Constructor
    def __init__(self, monster_definition):
        self.name = monster_definition["name"]
        self.image = monster_definition["image"]
        self.hit_points = random.randint(5, monster_definition["max_hit_points"])
        self.gold = random.randint(0, monster_definition["max_gold"])
        self.weapon = monster_definition["weapon"]
        self.level = monster_definition["level"]

    # Method to call when the monster attacks a character
    def triggered(self, character):
        # Calculate Damage Inflicted
        weapon = self.weapon
        damage = random.randint(0, weapon["damage"])
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
        return "The " + weapon["attack_message"] % (self.name, damage)


# This Function is to decide which monster to spawn in a given dungeon.
def pick_trap_for_dungeon_level(dungeon_id):
    if dungeon_id < 0:
        return None
    dungeon_monsters = []

    # Build a list of monsters that we could find in this dungeon
    # monster_leveling = 10 + (dungeon_id * 10)
    # log.info("Monster Leveling %d for Dungeon %d" % (monster_leveling, dungeon_id))
    # for index in range(len(all_monsters)):
    #     if all_monsters[index]["level"] < monster_leveling:
    #         dungeon_monsters.append(all_monsters[index])
    # # Select a monster appropriate for the level of this dungeon.
    # monster_id = random.randint(0, len(dungeon_monsters) - 1)
    # monster = Monster(dungeon_monsters[monster_id])
    # log.info("Monster Selected: %s, Level: %d for Dungeon %d" % (monster.name, monster.level, dungeon_id))
    # return monster


# Dictionaries of all Monsters in the Game

swarm_of_bees = {
    "name": "Swarm of Bees",
    "type": "monster",
    "level": 5,
    "image": images.swarm_of_bees,
    "max_hit_points": 20,
    "max_gold": 5,
    "weapon": items.bee_stinger
}

all_traps = [
    swarm_of_bees
]
