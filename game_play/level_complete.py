from game_play import db
from game_play import screen
from town import items


def process(game, level_id):
    title_image = 'L E V E L   ' + str(level_id + 1) + '   C O M P L E T E !'

    # Remove the map so the hero has to buy the next map.
    if items.dungeon_map in game.character.inventory:
        game.character.inventory.remove(items.dungeon_map)
    level = game.dungeon.levels[level_id]

    contents = "Monsters Killed........ " + str(level["monsters_killed"]) + "/" + str(level["monster_count"]) + "\n" \
               "Treasures Collected.... " + str(level["treasures_collected"]) + "/" + str(level["treasure_count"]) + "\n" \
               "Traps Triggered........ " + str(level["traps_triggered"]) + "/" + str(level["trap_count"]) + "\n" \
               "Level Step Bonus....... " + str(game.calc_score_level_bonus(level_id)) + "\n\n" \
               "HP Bonus Received...... " + str(game.calc_hp_bonus(level_id))
    game.character.level += 1

    # Update the Leaderboard
    game.status = "Playing: L" + str(level_id + 1)
    lb = db.load_leaderboard()
    lb.update_leader(game)
    db.save_leaderboard(lb)

    game.current_controller = 'town'

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
