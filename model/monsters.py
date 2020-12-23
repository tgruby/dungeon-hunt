import logging
import random
from view import images
from model import items

log = logging.getLogger('dragonsville')


# Class object to represent any active monster
class Monster:
    # Class Level Variables

    # Monster Constructor
    def __init__(self, monster_definition):
        self.name = monster_definition["name"]
        self.image = monster_definition["image"]
        self.hit_points = random.randint(5, monster_definition["max_hit_points"])
        self.gold = random.randint(1, monster_definition["max_gold"])
        self.weapon = monster_definition["weapon"]
        self.level = monster_definition["level"]

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
    # Select a monster appropriate for the level of this dungeon.
    monster_options = monsters_by_level[level_id]
    selected_monster = random.randint(0, len(monster_options) - 1)
    monster = Monster(monster_options[selected_monster])
    log.info("Monster Selected: %s, Level: %d for Dungeon %d" % (monster.name, monster.level, level_id))
    return monster


# Dictionaries of all Monsters in the Game

giant_rat = {
    "name": "Giant Rat",
    "type": "monster",
    "level": 4,
    "image": images.rat,
    "max_hit_points": 10,
    "max_gold": 10,
    "weapon": items.rat_teeth
}

giant_ant = {
    "name": "Giant Ant",
    "type": "monster",
    "level": 8,
    "image": images.giant_ant,
    "max_hit_points": 12,
    "max_gold": 12,
    "weapon": items.ant_pincers
}

angry_gnome = {
    "name": "Angry Gnome",
    "type": "monster",
    "level": 12,
    "image": images.gnome,
    "max_hit_points": 14,
    "max_gold": 18,
    "weapon": items.gnome_feet
}

badger = {
    "name": "Badger",
    "type": "monster",
    "level": 16,
    "image": images.badger,
    "max_hit_points": 16,
    "max_gold": 16,
    "weapon": items.badger_teeth
}

giant_spider = {
    "name": "Giant Spider",
    "type": "monster",
    "level": 18,
    "image": images.giant_spider,
    "max_hit_points": 18,
    "max_gold": 14,
    "weapon": items.spider_fangs
}

wolf = {
    "name": "Wolf",
    "type": "monster",
    "level": 28,
    "image": images.wolf,
    "max_hit_points": 40,
    "max_gold": 30,
    "weapon": items.wolf_teeth
}

goblin = {
    "name": "Goblin",
    "type": "monster",
    "level": 32,
    "image": images.goblin,
    "max_hit_points": 50,
    "max_gold": 60,
    "weapon": items.broad_sword
}
skeleton = {
    "name": "Skeleton",
    "type": "monster",
    "level": 46,
    "image": images.skeleton,
    "max_hit_points": 75,
    "max_gold": 100,
    "weapon": items.bony_fingers
}

vampire_bat = {
    "name": "Vampire Bat",
    "type": "monster",
    "level": 16,
    "image": images.vampire_bat,
    "max_hit_points": 30,
    "max_gold": 45,
    "weapon": items.bat_fangs
}

skeleton_warrior = {
    "name": "Skeleton Warrior",
    "type": "monster",
    "level": 96,
    "image": images.skeleton_warrior,
    "max_hit_points": 150,
    "max_gold": 150,
    "weapon": items.battle_axe
}

half_orc = {
    "name": "Half Orc",
    "type": "monster",
    "level": 128,
    "image": images.half_orc,
    "max_hit_points": 200,
    "max_gold": 300,
    "weapon": items.two_handed_sword
}

banshee = {
    "name": "Banshee",
    "type": "monster",
    "level": 164,
    "image": images.banshee,
    "max_hit_points": 250,
    "max_gold": 400,
    "weapon": items.banshee_scream
}

minotaur = {
    "name": "Minotaur",
    "type": "monster",
    "level": 256,
    "image": images.minotaur,
    "max_hit_points": 350,
    "max_gold": 600,
    "weapon": items.dragonbane
}

red_dragon = {
    "name": "Red Dragon",
    "type": "monster",
    "level": 512,
    "image": images.dragon,
    "max_hit_points": 500,
    "max_gold": 2000,
    "weapon": items.fireball
}

all_monsters = [
    giant_rat,
    wolf,
    giant_ant,
    giant_spider,
    angry_gnome,
    badger,
    skeleton,
    vampire_bat,
    goblin,
    skeleton_warrior,
    half_orc,
    banshee,
    minotaur
]

monsters_by_level = [
    [
        giant_rat,
        giant_ant,
        giant_spider,
        badger
    ],
    [
        wolf,
        angry_gnome,
        badger,
        vampire_bat,
        goblin,
    ],
    [
        wolf,
        angry_gnome,
        skeleton,
        skeleton,
        skeleton,
        vampire_bat,
        goblin,
        skeleton_warrior,
        skeleton_warrior,
        skeleton_warrior,
    ],
    [
        skeleton,
        vampire_bat,
        goblin,
        skeleton_warrior,
        half_orc,
        banshee,
        minotaur
    ]]
