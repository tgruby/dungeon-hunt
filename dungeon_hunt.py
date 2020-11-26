from flask import Flask, render_template, jsonify
import os
from controller import router, dungeon_design_router

# TODO: Add ability to have different players play at the same time (different heros, different dungeons)
# TODO: End Game when killed or hit dragon (put person on leaderboard).
# TODO: Add scoring: 20 points for killing a monster (x level), 10 for finding treasures.
# TODO: Create Leaderboard (5 deep).
# TODO: possibly add strength and resistance potions.

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


# Receive a game play command from the browser and respond with a json object representing each panel.
@app.route('/game/action/<action>')
def process_action(action):
    return jsonify(router.process(action)), 200


# Receive a game play command from the browser and respond with a json object representing each panel.
@app.route('/game/action/')
def process_no_action(action):
    return jsonify(router.process(None)), 200


if __name__ == '__main__':
    app.run()
