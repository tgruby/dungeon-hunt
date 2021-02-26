import random
from town import items, potions


class Character:
    # Global Class Variables

    # Character Constructor (for our hero)
    def __init__(self, character_definition):
        self.type = character_definition["type"]
        self.max_hit_points = character_definition["hit_points"]
        self.hit_points = self.max_hit_points
        self.gold = character_definition["gold"]
        self.equipped_weapon = character_definition["equipped_weapon"]
        self.equipped_armor = character_definition["equipped_armor"]
        self.equipped_shield = character_definition["equipped_shield"]
        self.inventory = character_definition["inventory"]
        # Instantiate a point of view object.  This will help us render the view of the character
        self.view = None
        self.clairvoyance_count = 0
        self.step_count = 0

    def add_to_inventory(self, item):
        pass

    # Return True if the character is alive, False if not.
    def is_alive(self):
        return self.hit_points > 0

    # Function that processes an attack of any character on another character
    def attack_monster(self, monster):
        if monster is not None:
            weapon = self.equipped_weapon
            damage = random.randint(0, weapon["damage"])
            monster.hit_points -= damage
            message = weapon["attack_message"] % ('You', damage)
            return message

    def take_damage(self, damage_inflicted):
        # Calculate Damage prevented by protection
        protection = 0
        if self.equipped_armor is not None:
            protection += random.randint(4, -self.equipped_armor["damage"])
        if self.equipped_shield is not None:
            protection += random.randint(4, -self.equipped_shield["damage"])
        damage = damage_inflicted - protection
        # Prevent damage from being negative (healing the hero)
        if damage < 0:
            damage = 0
        # Subtract the damage from our hero's hit points
        self.hit_points -= damage
        return damage


warrior = {
    "name": None,
    "type": "warrior",
    "hit_points": 20,
    "gold": 50,
    "equipped_weapon": items.dagger,
    "equipped_armor": None,
    "equipped_shield": None,
    "inventory": [items.dagger, potions.health_potion, potions.health_potion],
    "level_up_hit_points": 15
}
