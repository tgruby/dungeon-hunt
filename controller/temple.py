import sys
import view.screen
from view import screen, images
from controller import router, town

commands = "(F)ull Healing, (P)artial Healing, (L)eave Temple"
message = "Welcome to Wudang Five Immortals Temple, weary traveler. How can we help you?"
image = images.tall_temple


#  This function controls the interactions at the temple.
def enter(our_hero):
    print("temple.enter")
    router.current_controller = sys.modules[__name__]

    return screen.paint(
        hero=our_hero,
        commands=commands,
        messages=message,
        left_pane_content=image,
        right_pane_content=draw_healing_list(our_hero),
        sound=None,
        sleep=100
    )


def process(our_hero, action):
    print("temple.process: " + action)

    # Full Healing
    if action.lower() == "f":
        if our_hero.hit_points != our_hero.max_hit_points:  # Make sure we need healing
            if our_hero.gold >= full_price(our_hero):
                our_hero.gold = our_hero.gold - full_price(our_hero)
                our_hero.hit_points = our_hero.max_hit_points
                message = "The temple priests pray over you and you are fully healed!"
            else:
                message = "You do not have enough gold!"
        else:
            message = "You are healthy! You don't need healing!"

        return screen.paint(
            hero=our_hero,
            commands=commands,
            messages=message,
            left_pane_content=image,
            right_pane_content=draw_healing_list(our_hero),
            sound=None,
            sleep=100
        )

    # Half Healing
    if action.lower() == "p":
        if our_hero.hit_points != our_hero.max_hit_points:  # Make sure we need healing
            if our_hero.gold >= half_price(our_hero):
                our_hero.gold -= half_price(our_hero)
                our_hero.hit_points += half_percent(our_hero)
                message = "The temple priests pray over you and you feel much better!"
            else:
                message = "You do not have enough gold!"
        else:
            message = "You are healthy! You don't need healing!"

        return screen.paint(
            hero=our_hero,
            commands=commands,
            messages=message,
            left_pane_content=image,
            right_pane_content=draw_healing_list(our_hero),
            sound=None,
            sleep=100
        )

    # Leave and go back to the town
    if action.lower() == "l":
        return town.enter(our_hero)

    # All else fails, just repost this page
    return enter(our_hero)


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
