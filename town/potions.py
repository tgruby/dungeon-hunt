

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


def use_potion(potion, game):
    hero = game.character
    msg = ''
    if potion["id"] == 'heal':
        if hero.hit_points == hero.max_hit_points:
            msg = "You don't need that right now."
        else:
            hero.hit_points = hero.max_hit_points
            hero.inventory.remove(potion)
            msg = "You drank the %s and a warm fuzzy feeling comes over you." % potion["name"]
    elif potion["id"] == 'teleport':
        hero.view.set_starting_position()  # put character back at the start of dungeon level 0.
        game.current_controller = 'town'
        hero.inventory.remove(potion)
        msg = "You drank the %s and your vision swims and everything goes dark! You awake in town." \
              % potion["name"]
    elif potion["id"] == 'clairvoyance':
        hero.clairvoyance_count += 100
        hero.inventory.remove(potion)
        msg = "You drank the %s and your mind sharpens.  You instantly know the entire layout of the labyrinth!" \
              % potion["name"]

    return msg


# Dictionaries of potions in the Game
health_potion = {
    "id": 'heal',
    "name": "Healing Potion",
    "description": "This potion will fully restore you, like a younger Gandolf!",
    "type": "potion",
    "max_hit_points": 1,
    "affects": "character",
    "cost": 2
}

teleport_potion = {
    "id": 'teleport',
    "name": "Teleport Potion",
    "description": "This potion will get you out of a deep jam if stuck in the labyrinth and bring you back to town!",
    "type": "potion",
    "max_hit_points": 1,
    "affects": "character",
    "cost": 2
}

clairvoyance_potion = {
    "id": 'clairvoyance',
    "name": "Clairvoyance Potion",
    "description": "This potion will enable your mind to see the entire labyrinth for a short time",
    "type": "potion",
    "affects": "character",
    "cost": 2
}

all_enchantments = [
    health_potion,
    teleport_potion,
    clairvoyance_potion
]
