

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

half_health_potion = {
    "name": "Watered Down Healing Potion",
    "description": "This potion will refresh you, sort of...",
    "type": "potion",
    "max_hit_points": .5,
    "affects": "character",
    "cost": 25
}

full_health_potion = {
    "name": "Good Stuff Healing Potion",
    "description": "This potion will fully restore you, like a young Gandolf!",
    "type": "potion",
    "max_hit_points": 1,
    "affects": "character",
    "cost": 50
}

all_enchantments = [
    half_health_potion,
    full_health_potion
]
