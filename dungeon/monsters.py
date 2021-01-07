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
        self.gold = random.randint(3, monster_definition["gold"])
        self.attack_damage = monster_definition["attack_damage"]
        self.attack_description = monster_definition["attack_description"]
        self.is_boss = monster_definition["is_boss"]
        self.item_dropped = monster_definition["item_dropped"]

    # Method to call when the monster attacks a character
    def attack(self, character):
        # Calculate Damage Inflicted
        damage = random.randint(0, self.attack_damage)
        adjusted_damage = character.take_damage(damage)
        return "The " + self.attack_description % (self.name, adjusted_damage)

    def is_alive(self):
        return self.hit_points > 0


# This Function is to decide which monster to spawn in a given dungeon.
def get_a_monster_for_dungeon_level(level_id):
    # Select a monster appropriate for the level of this dungeon.
    # Use a sliding scale of 4 monsters per level.
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
    if level_id == 5:
        return Monster(giant_snake)
    elif level_id == 10:
        return Monster(cyclops)
    elif level_id == 15:
        return Monster(wraith)
    else:
        return Monster(red_dragon)


# Dictionaries of all Monsters in the Game

giant_rat = {
    "name": "Giant Rat",
    "is_boss": False,
    "image": images.rat,
    "hit_points": 8,
    "gold": 10,
    "attack_damage": items.rat_teeth["damage"],
    "attack_description": items.rat_teeth["attack_message"],
    "item_dropped": items.rat_teeth
}

giant_ant = {
    "name": "Giant Ant",
    "is_boss": False,
    "image": images.giant_ant,
    "hit_points": 12,
    "gold": 12,
    "attack_damage": items.ant_pincers["damage"],
    "attack_description": items.ant_pincers["attack_message"],
    "item_dropped": items.ant_pincers
}

angry_gnome = {
    "name": "Angry Gnome",
    "is_boss": False,
    "image": images.gnome,
    "hit_points": 14,
    "gold": 18,
    "attack_damage": items.gnome_feet["damage"],
    "attack_description": items.gnome_feet["attack_message"],
    "item_dropped": items.gnome_feet
}

giant_snake = {
    "name": "Giant Snake",
    "is_boss": True,
    "image": images.giant_snake,
    "hit_points": 42,
    "gold": 34,
    "attack_damage": items.snake_bite["damage"],
    "attack_description": items.snake_bite["attack_message"],
    "item_dropped": items.lucky_rock
}

badger = {
    "name": "Badger",
    "is_boss": False,
    "image": images.badger,
    "hit_points": 16,
    "gold": 16,
    "attack_damage": items.badger_teeth["damage"],
    "attack_description": items.badger_teeth["attack_message"],
    "item_dropped": items.badger_teeth
}

giant_spider = {
    "name": "Giant Spider",
    "is_boss": False,
    "image": images.giant_spider,
    "hit_points": 18,
    "gold": 14,
    "attack_damage": items.spider_fangs["damage"],
    "attack_description": items.spider_fangs["attack_message"],
    "item_dropped": items.spider_fangs
}

wolf = {
    "name": "Wolf",
    "is_boss": False,
    "image": images.wolf,
    "hit_points": 32,
    "gold": 30,
    "attack_damage": items.wolf_teeth["damage"],
    "attack_description": items.wolf_teeth["attack_message"],
    "item_dropped": items.wolf_teeth
}

vampire_bat = {
    "name": "Vampire Bat",
    "is_boss": False,
    "image": images.vampire_bat,
    "hit_points": 32,
    "gold": 45,
    "attack_damage": items.bat_fangs["damage"],
    "attack_description": items.bat_fangs["attack_message"],
    "item_dropped": items.bat_fangs
}

goblin = {
    "name": "Goblin",
    "is_boss": False,
    "image": images.goblin,
    "hit_points": 42,
    "gold": 60,
    "attack_damage": items.broad_sword["damage"],
    "attack_description": items.broad_sword["attack_message"],
    "item_dropped": items.broad_sword
}

skeleton = {
    "name": "Skeleton",
    "is_boss": False,
    "image": images.skeleton,
    "hit_points": 54,
    "gold": 100,
    "attack_damage": items.bony_fingers["damage"],
    "attack_description": items.bony_fingers["attack_message"],
    "item_dropped": items.bony_fingers
}

skeleton_warrior = {
    "name": "Skeleton Warrior",
    "is_boss": False,
    "image": images.skeleton_warrior,
    "hit_points": 72,
    "gold": 150,
    "attack_damage": items.battle_axe["damage"],
    "attack_description": items.battle_axe["attack_message"],
    "item_dropped": items.battle_axe
}

half_orc = {
    "name": "Half Orc",
    "is_boss": False,
    "image": images.half_orc,
    "hit_points": 64,
    "gold": 128,
    "attack_damage": items.broad_sword["damage"],
    "attack_description": items.broad_sword["attack_message"],
    "item_dropped": items.two_handed_sword
}

minotaur = {
    "name": "Minotaur",
    "is_boss": False,
    "image": images.minotaur,
    "hit_points": 96,
    "gold": 196,
    "attack_damage": items.two_handed_sword["damage"],
    "attack_description": items.two_handed_sword["attack_message"],
    "item_dropped": items.two_handed_sword
}

cyclops = {
    "name": "Cyclops",
    "is_boss": True,
    "image": images.cyclops,
    "hit_points": 128,
    "gold": 128,
    "attack_damage": items.broad_sword["damage"],
    "attack_description": items.broad_sword["attack_message"],
    "item_dropped": items.elvin_sword
}

wraith = {
    "name": "Wraith",
    "is_boss": True,
    "image": images.wraith,
    "hit_points": 256,
    "gold": 250,
    "attack_damage": items.wraith_touch["damage"],
    "attack_description": items.wraith_touch["attack_message"],
    "item_dropped": items.shield_of_protection
}

red_dragon = {
    "name": "Red Dragon",
    "is_boss": True,
    "image": images.dragon,
    "hit_points": 512,
    "gold": 2000,
    "attack_damage": items.fireball["damage"],
    "attack_description": items.fireball["attack_message"],
    "item_dropped": items.dragon_skin_armor
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

