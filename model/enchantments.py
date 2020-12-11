

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


# Dictionaries of all enchantments in the Game
# TODO: Add a potion to teleport hero back to town

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

all_enchantments = [
    health_potion,
    gandalfs_granola
]
