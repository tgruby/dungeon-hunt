

# Class object to represent any active monster
class Potion:
    # Class Level Variables

    # Potion Constructor
    def __init__(self, enchantment_type):
        self.name = enchantment_type["name"]
        self.description = enchantment_type["description"]
        self.type = enchantment_type["type"]
        self.hit_points = enchantment_type["max_hit_points"]
        self.gold = enchantment_type["cost"]


# Dictionaries of potions in the Game

half_health_potion = {
    "id": 'half_heal',
    "name": "Watered Down Healing Potion",
    "description": "This potion will refresh you, sort of...",
    "type": "potion",
    "max_hit_points": .5,
    "affects": "character",
    "cost": 15
}

full_health_potion = {
    "id": 'full_heal',
    "name": "Good Stuff Healing Potion",
    "description": "This potion will fully restore you, like a younger Gandolf!",
    "type": "potion",
    "max_hit_points": 1,
    "affects": "character",
    "cost": 30
}

teleport_potion = {
    "id": 'teleport',
    "name": "Teleport Potion",
    "description": "This potion will get you out of a deep jam if stuck in the catacombs and bring you back to town!",
    "type": "potion",
    "max_hit_points": 1,
    "affects": "character",
    "cost": 50
}

all_enchantments = [
    half_health_potion,
    full_health_potion,
    teleport_potion
]
