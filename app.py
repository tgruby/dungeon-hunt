import os
import db
import uuid
from model import games
from controller import get_gamer_tag
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
    return render_template('game.html')


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
        # Create a new game
        game = db.load_game(str(uuid.uuid4()))
        game.current_controller = 'get_gamer_tag'
        session['game_id'] = game.game_id  # Save game id to session.
        db.save_game(game.game_id, game)
        # Now request a gamer tag.
        return jsonify(get_gamer_tag.process(game, None)), 200
    else:
        gid = session['game_id']
        game = db.load_game(gid)

        if game.game_over:
            # Character has been killed.  Add to leaderboard, cleanup game.
            lb = db.load_leaderboard()
            lb.add_leader(game)
            db.save_leaderboard(lb)
            db.delete_game(gid)
            session.clear()
            return jsonify(get_gamer_tag.process(game, None)), 200
        else:
            # Just run the game route.
            update = games.route(game, action)
            db.save_game(gid, game)
            return jsonify(update), 200


if __name__ == '__main__':
    app.run()
