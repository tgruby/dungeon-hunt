import logging

log = logging.getLogger('dragonsville')


# Class object to represent any active monster
class EnchantedItem:
    # Class Level Variables

    # Monster Constructor
    def __init__(self, enchantment_type):
        self.name = enchantment_type["name"]
        self.description = enchantment_type["description"]
        self.type = enchantment_type["type"]
        self.hit_points = enchantment_type["max_hit_points"]
        self.gold = enchantment_type["cost"]

    # Method to call when the monster attacks a character
    def use_item(self, our_hero, item, monster):
        if self.type == "potion":
            # TODO: Add logic to do damage to the creature and remove the item, return attack message.
            pass
        elif self.type == "scroll":
            # TODO: Add logic to do damage to the creature and remove the item, return attack message.
            pass


# Dictionaries of all enchantments in the Game

health_potion = {
    "name": "Simple Healing Potion",
    "description": "This potion will refresh you, making you feel ready for the next battle.",
    "type": "potion",
    "max_hit_points": 25,
    "affects": "character",
    "cost": 25
}

gandalfs_granola = {
    "name": "Gandalf's Healing Granola",
    "description": "This Granola bar will make you feel young again, like Gandolf!",
    "type": "potion",
    "max_hit_points": 100,
    "affects": "character",
    "cost": 75
}

super_scroll= {
    "name": "Earthquake Scroll",
    "description": "This Scroll, when read, creates an earthquake sending stone and debris down onto the head of your "
                   "foes. ",
    "type": "scroll",
    "max_hit_points": 200,
    "affects": "character",
    "cost": 500
}

all_enchantments = [
    health_potion,
    gandalfs_granola,
    super_scroll
]
