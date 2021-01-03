import logging
import random
from game_play import images
from town import items

log = logging.getLogger('dragonsville')


# Class object to represent any active monster
class Monster:
    # Class Level Variables

    # Monster Constructor
    def __init__(self, monster_definition):
        self.name = monster_definition["name"]
        self.image = monster_definition["image"]
        self.hit_points = monster_definition["hit_points"]
        self.gold = random.randint(3, monster_definition["max_gold"])
        self.weapon = monster_definition["weapon"]
        self.is_boss = monster_definition["is_boss"]
        self.special_drop = monster_definition["special_drop"]

    # Method to call when the monster attacks a character
    def attack(self, character):
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

    def is_alive(self):
        return self.hit_points > 0


# This Function is to decide which monster to spawn in a given dungeon.
def get_a_monster_for_dungeon_level(level_id):
    # Select a monster appropriate for the level of this dungeon. If this is the first dungeon, just return the rat.
    if level_id == 0:
        return Monster(dungeon_monsters[0])

    suitable_monsters = []
    upper_bounds = level_id
    if upper_bounds >= len(dungeon_monsters):
        upper_bounds = len(dungeon_monsters)-1
    lower_bounds = upper_bounds - 4
    if lower_bounds < 0:
        lower_bounds = 0

    while lower_bounds <= upper_bounds:
        suitable_monsters.append(dungeon_monsters[lower_bounds])
        lower_bounds += 1

    selected_monster = random.randint(0, len(suitable_monsters) - 1)
    return Monster(suitable_monsters[selected_monster])


# This Function is to decide which monster boss to spawn in a given dungeon.
def get_boss_for_dungeon_level(level_id):
    # Select a monster appropriate for the level of this dungeon. If this is the first dungeon, just return the rat.
    if level_id < 7:
        return Monster(monster_bosses[0])
    elif level_id < 12:
        return Monster(monster_bosses[1])
    elif level_id < 17:
        return Monster(monster_bosses[2])
    else:
        return Monster(monster_bosses[3])


# Dictionaries of all Monsters in the Game

giant_rat = {
    "name": "Giant Rat",
    "type": "monster",
    "is_boss": False,
    "image": images.rat,
    "hit_points": 8,
    "max_gold": 10,
    "weapon": items.rat_teeth,
    "special_drop": None
}

giant_ant = {
    "name": "Giant Ant",
    "type": "monster",
    "is_boss": False,
    "image": images.giant_ant,
    "hit_points": 12,
    "max_gold": 12,
    "weapon": items.ant_pincers,
    "special_drop": None
}

angry_gnome = {
    "name": "Angry Gnome",
    "type": "monster",
    "is_boss": False,
    "image": images.gnome,
    "hit_points": 14,
    "max_gold": 18,
    "weapon": items.gnome_feet,
    "special_drop": None
}

giant_snake = {
    "name": "Giant Snake",
    "type": "monster",
    "is_boss": True,
    "image": images.giant_snake,
    "hit_points": 42,
    "max_gold": 34,
    "weapon": items.snake_bite,
    "special_drop": items.lucky_rock
}

badger = {
    "name": "Badger",
    "type": "monster",
    "is_boss": False,
    "image": images.badger,
    "hit_points": 16,
    "max_gold": 16,
    "weapon": items.badger_teeth,
    "special_drop": None
}

giant_spider = {
    "name": "Giant Spider",
    "type": "monster",
    "is_boss": False,
    "image": images.giant_spider,
    "hit_points": 18,
    "max_gold": 14,
    "weapon": items.spider_fangs,
    "special_drop": None
}

wolf = {
    "name": "Wolf",
    "type": "monster",
    "is_boss": False,
    "image": images.wolf,
    "hit_points": 32,
    "max_gold": 30,
    "weapon": items.wolf_teeth,
    "special_drop": None
}

vampire_bat = {
    "name": "Vampire Bat",
    "type": "monster",
    "is_boss": False,
    "image": images.vampire_bat,
    "hit_points": 32,
    "max_gold": 45,
    "weapon": items.bat_fangs,
    "special_drop": None
}

goblin = {
    "name": "Goblin",
    "type": "monster",
    "is_boss": False,
    "image": images.goblin,
    "hit_points": 42,
    "max_gold": 60,
    "weapon": items.broad_sword,
    "special_drop": None
}

skeleton = {
    "name": "Skeleton",
    "type": "monster",
    "is_boss": False,
    "image": images.skeleton,
    "hit_points": 54,
    "max_gold": 100,
    "weapon": items.bony_fingers,
    "special_drop": None
}

skeleton_warrior = {
    "name": "Skeleton Warrior",
    "type": "monster",
    "is_boss": False,
    "image": images.skeleton_warrior,
    "hit_points": 72,
    "max_gold": 150,
    "weapon": items.battle_axe,
    "special_drop": None
}

half_orc = {
    "name": "Half Orc",
    "type": "monster",
    "is_boss": False,
    "image": images.half_orc,
    "hit_points": 64,
    "max_gold": 128,
    "weapon": items.broad_sword,
    "special_drop": None
}

minotaur = {
    "name": "Minotaur",
    "type": "monster",
    "is_boss": False,
    "image": images.minotaur,
    "hit_points": 96,
    "max_gold": 196,
    "weapon": items.two_handed_sword,
    "special_drop": None
}

cyclops = {
    "name": "Cyclops",
    "type": "monster",
    "is_boss": True,
    "image": images.cyclops,
    "hit_points": 128,
    "max_gold": 256,
    "weapon": items.two_handed_sword,
    "special_drop": items.elvin_sword
}

wraith = {
    "name": "Wraith",
    "type": "monster",
    "is_boss": True,
    "image": images.wraith,
    "hit_points": 256,
    "max_gold": 250,
    "weapon": items.wraith_touch,
    "special_drop": items.shield_of_protection
}

red_dragon = {
    "name": "Red Dragon",
    "type": "monster",
    "is_boss": True,
    "image": images.dragon,
    "hit_points": 512,
    "max_gold": 2000,
    "weapon": items.fireball,
    "special_drop": items.dragon_skin_armor
}

dungeon_monsters = [
    giant_rat,
    giant_ant,
    giant_spider,
    badger,
    wolf,
    angry_gnome,
    vampire_bat,
    skeleton,
    goblin,
    skeleton_warrior,
    half_orc,
    minotaur
]

monster_bosses = [
    giant_snake,
    cyclops,
    wraith,
    red_dragon
]
