import os
from controller import router, init_game
from flask import Flask, render_template, jsonify, session

# TODO: Add gamertag into session
# TODO: fix death.  should end game and go to leaderboard.
# TODO: folks miss stuff when fighting... they just jam f to fight.  have a time lag during fighting? or switch to c. for continue...
# TODO: Add ability to have different players play at the same time (different heros, different dungeons)
# TODO: End Game when killed or hit dragon (put person on leaderboard).
# TODO: Add scoring: 20 points for killing a monster (x level), 10 for finding treasures.
# TODO: Create Leaderboard (5 deep).
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


# Receive a game play command from the browser and respond with a json object representing each panel.
@app.route('/api/v1/splash-screen')
def splash_screen():
    # If someone is starting the game, specialized logic for game start since a hero and dungeon need to be created.
    return jsonify(init_game.show_splash()), 200


# Receive a game play command from the browser and respond with a json object representing each panel.
@app.route('/api/v1/start/action/')
def undefined_start_game_request():
    # If someone is starting the game, specialized logic for game start since a hero and dungeon need to be created.
    return jsonify(init_game.process(' ')), 200


# Receive a game play command from the browser and respond with a json object representing each panel.
@app.route('/api/v1/start/action/<action>')
def process_start_game(action):
    # If someone is starting the game, specialized logic for game start since a hero and dungeon need to be created.
    return jsonify(init_game.process(action)), 200


# Receive a blank game command... respond with a response.
@app.route('/api/v1/game/<token>/action/')
def process_no_action(token):
    return jsonify(router.process(token, None)), 200


# Receive a game play command and respond with a json object representing each panel.
@app.route('/api/v1/game/<token>/action/<action>')
def process_action(token, action):
    return jsonify(router.process(token, action)), 200


# Receive a game play command and respond with a json object representing each panel.
@app.route('/api/v1/gamertag/<tag>')
def process_gamertag(tag):
    session['gamertag'] = tag
    return jsonify('{ok}'), 200


if __name__ == '__main__':
    app.run()
