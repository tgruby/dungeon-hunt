import os

import game_play
from game_play import db, leader_board
from datetime import datetime
from flask import Flask, render_template, jsonify, session


# Set the directory where we store web resources
app = Flask(
    __name__,
    static_url_path='/resources',
    static_folder="www-resources",
    template_folder="www",
    instance_relative_config=True
)
app.config.from_mapping(SECRET_KEY='billy_bobby_bruno_beats_a_basket')


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

        # Clean up a broken game where there is no game file but there is a session token.
        if game is None:
            session.clear()
            return jsonify(leader_board.process(None, None)), 200

        if game.game_over:
            # Character has been killed.  Add to gamer_tag (action) to leaderboard, cleanup game.
            game.gamer_tag = action
            if game.gamer_tag is not None:
                lb = db.load_leaderboard()
                lb.add_leader(game)
                db.save_leaderboard(lb)
            db.delete_game(gid)
            session.clear()
            return jsonify(leader_board.process(None, None)), 200
        else:
            # Just run the game route.
            update = game_play.route(game, action)
            db.save_game(gid, game)
            return jsonify(update), 200


# Receive a game play command and respond with a json object representing each panel.
@app.route('/api/v1/game/end-game')
def end_game():
    if 'game_id' in session:
        game_id = session['game_id']
        print('Ending Game: ' + game_id)
        db.delete_game(game_id)
    session.clear()
    return jsonify('{ok}'), 200


if __name__ == '__main__':
    app.run()
