import view.screen
from view import screen, images
from controller import town

commands = "(F)ull Healing, (P)artial Healing, (L)eave Temple"
message = "Welcome to Wudang Five Immortals Temple, weary traveler. How can we help you?"
image = images.tall_temple


#  This function controls the interactions at the temple.
def paint(our_hero, msg):

    return screen.paint_two_panes(
        hero=our_hero,
        commands=commands,
        messages=msg,
        left_pane_content=image,
        right_pane_content=draw_healing_list(our_hero),
        sound=None,
        delay=0,
        interaction_type='enter_press'
    )


def process(game, action):
    our_hero = game.character

    if action is None:
        return paint(our_hero, message)

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

        return paint(our_hero, msg)

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

        return paint(our_hero, msg)

    # Leave and go back to the town
    if action.lower() == "l":
        game.current_controller = 'town'
        return town.process(game, None)

    # All else fails, just repost this page
    return paint(our_hero, message)


def full_price(our_hero):
    return round((our_hero.max_hit_points - our_hero.hit_points) / 2)


def half_price(our_hero):
    return round(full_price(our_hero) / 2)


def half_percent(our_hero):
    full_percent = round(our_hero.max_hit_points - our_hero.hit_points)
    return round(full_percent / 2)


# List out the various healing that our hero can have
def draw_healing_list(our_hero):
    border = "<================<o>================>\n"
    full_percent = round(our_hero.max_hit_points - our_hero.hit_points)

    response = border
    response += " Description     | % Healed | Cost" + '\n'
    response += border
    response += " Full Healing    | " + view.screen.front_padding(str(full_percent), 7) + "% | " \
                + view.screen.front_padding(str(full_price(our_hero)), 4) + '\n'
    response += " Partial Healing | " + view.screen.front_padding(str(half_percent(our_hero)), 7) + "% | " \
                + view.screen.front_padding(str(half_price(our_hero)), 4) + '\n'
    response += border
    return response
