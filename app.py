import os
import db
from datetime import datetime
from model import games
from controller import leader_board
from flask import Flask, render_template, jsonify, session

# TODO: fix screen refresh and putting character back into the game where they left off.
# TODO: if character has been killed, fix removing the game-token and forcing back to the start screen.
# TODO: fix death by trap.  should end game and go to leaderboard.
# TODO: Add ability to have different players play at the same time (different heros, different dungeons)
# TODO: End Game when killed or hit dragon (put person on leaderboard).
# TODO: possibly add strength and resistance potions.
# TODO: should you be able to buy a teleport out of the dungeon?
# TODO: don't know what is a shield, armor, or weapon.
# TODO: descriptions for more things?

# Set the directory where we store web resources
app = Flask(__name__, static_url_path='/static', instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='billy_bobby_bruno_beats_a_basket',
    DATABASE=os.path.join(app.instance_path, 'dungeon_hunt.sqlite'),
)


# Return our root page (terminal)
@app.route('/')
def root():
    last_modified = datetime.fromtimestamp(os.stat('app.py').st_mtime)
    return render_template('game.html', last_updated=last_modified)


# Receive a blank game command... respond with a response.
@app.route('/api/v1/game/action/')
def process_no_action():
    # process action for this game.
    return process_action(None)


# Receive a game play command and respond with a json object representing each panel.
@app.route('/api/v1/game/action/<action>')
def process_action(action):
    # The first thing we check is if we have a game.  If not, we need to create a new game to track this user's
    # interaction.
    if 'game_id' not in session:
        response = leader_board.process(None, action)
        if 'game_id' in response and response.get('game_id') is not None:
            session['game_id'] = response.get('game_id')  # Save game id to session.
        return jsonify(response), 200
    else:
        gid = session['game_id']
        game = db.load_game(gid)

        if game.game_over:
            # Character has been killed.  Add to gamer_tag (action) to leaderboard, cleanup game.
            game.gamer_tag = action
            print('Saving Gamer Tag: ' + action)
            lb = db.load_leaderboard()
            lb.add_leader(game)
            db.save_leaderboard(lb)
            db.delete_game(gid)
            session.clear()
            return jsonify(leader_board.process(None, None)), 200
        else:
            # Just run the game route.
            update = games.route(game, action)
            db.save_game(gid, game)
            return jsonify(update), 200


if __name__ == '__main__':
    app.run()
