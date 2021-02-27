import game_play.screen
from game_play import images, screen
import town

commands = "(F)ull Healing, (P)artial Healing, E(x)it Temple"
message = "Welcome to Wudang Five Immortals Temple, weary traveler. How can we help you?"
image = images.tall_temple


#  This function controls the interactions at the temple.
def paint(game, msg):

    return screen.paint_two_panes(
        game=game,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=draw_healing_list(game.character),
        sound=None,
        delay=0,
        interaction_type='key_press'
    )


def process(game, action):
    our_hero = game.character

    if action is None:
        return paint(game, message)

    # Full Healing
    if action.lower() == "f":
        if our_hero.hit_points != our_hero.max_hit_points:  # Make sure we need healing
            if our_hero.gold >= full_price(our_hero):
                our_hero.gold = our_hero.gold - full_price(our_hero)
                our_hero.hit_points = our_hero.max_hit_points
                msg = "The temple priests pray over you and you are fully healed!"
            else:
                msg = "You do not have enough gold!"
        else:
            msg = "You are healthy! You don't need healing!"

        return paint(game, msg)

    # Half Healing
    if action.lower() == "p":
        if our_hero.hit_points != our_hero.max_hit_points:  # Make sure we need healing
            if our_hero.gold >= half_price(our_hero):
                our_hero.gold -= half_price(our_hero)
                our_hero.hit_points += half_percent(our_hero)
                msg = "The temple priests pray over you and you feel much better!"
            else:
                msg = "You do not have enough gold!"
        else:
            msg = "You are healthy! You don't need healing!"

        return paint(game, msg)

    # Leave and go back to the town
    if action.lower() == "x":
        game.current_controller = 'town'
        return town.process(game, None)

    # All else fails, just repost this page
    return paint(game, message)


def full_price(hero):
    if hero.hit_points == hero.max_hit_points:
        return 0
    # Have the price cost 20% of hero's gold or 6 gold, whichever is more.
    cost = hero.gold * 0.2
    if cost > 6:
        return round(cost)
    return 6


def half_price(hero):
    if hero.hit_points == hero.max_hit_points:
        return 0
    return round(full_price(hero) / 2)


def half_percent(our_hero):
    full_percent = round(our_hero.max_hit_points - our_hero.hit_points)
    return round(full_percent / 2)


# List out the various healing that our hero can have
def draw_healing_list(our_hero):
    full_percent = round(our_hero.max_hit_points - our_hero.hit_points)

    response = game_play.screen.medium_border + '\n'
    response += "  Description              | % Healed | Cost" + '\n'
    response += game_play.screen.medium_border + '\n'
    response += "  Full Healing             | " + game_play.screen.front_padding(str(full_percent), 7) + "% | " \
                + game_play.screen.front_padding(str(full_price(our_hero)), 4) + '\n'
    response += "  Partial Healing          | " + game_play.screen.front_padding(str(half_percent(our_hero)), 7) + "% | " \
                + game_play.screen.front_padding(str(half_price(our_hero)), 4) + '\n'
    response += game_play.screen.medium_border + '\n'
    return response
