from town import items
from dungeon import monsters
from game_play import db, screen, game_won


def process(game, boss_defeated, monster):
    level_id = game.dungeon.current_level_id
    game.dungeon.complete_level()
    if monster is not None and monster.name == monsters.red_dragon["name"]:
        game.calc_score_level_bonus()
        game.calc_boss_bonus()
        return game_won.process(game, None)
    else:
        title_image = 'L E V E L   ' + str(level_id) + '   C O M P L E T E !'

    # Remove the map so the hero has to buy the next map.
    if items.dungeon_map in game.character.inventory:
        game.character.inventory.remove(items.dungeon_map)
    level = game.dungeon.current_level

    contents = "Monsters Killed........ " + str(level["monsters_killed"]) + "/" + str(level["monster_count"]) + "\n" \
               "Treasures Collected.... " + str(level["treasures_collected"]) + "/" + str(level["treasure_count"]) + "\n" \
               "Traps Triggered........ " + str(level["traps_triggered"]) + "/" + str(level["trap_count"]) + "\n" \
               "Level Step Bonus....... " + str(game.calc_score_level_bonus()) + "\n\n" \
               "HP Bonus Received...... " + str(game.calc_hp_bonus())

    game.current_controller = 'town'

    if boss_defeated:
        contents += "\n\nDefeat Boss Bonus... " + str(game.calc_boss_bonus())
        game.character.inventory.append(monster.item_dropped)
        contents += "\n" + monster.name + " Dropped... " + monster.item_dropped["name"] + "!!!"
        # contents += "\n" + monster.name + " Dropped... an extra Skeleton Key!!!"

    # Update the Leaderboard
    game.status = "Completed: L" + str(level_id)
    lb = db.load_leaderboard()
    lb.update_leader(game)
    db.save_leaderboard(lb)

    return screen.paint_one_pane(
        title_image=title_image,
        contents=None,
        contents_image=contents,
        commands="Hit any key to continue...",
        sound='level-complete',
        delay=2000,
        animation='confetti',
        interaction_type='key_press',
        game_id=game.game_id
    )
