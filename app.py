import os
import uuid
from controller import router, leader_board, intro
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


# Receive a game play command and respond with a json object representing each panel.
@app.route('/api/v1/gamer-tag/<tag>')
def set_gamer_tag(tag):
    session['gamer_tag'] = tag
    return jsonify('{ok}'), 200


# Return the Splash Screen, which is the LeaderBoard page.
@app.route('/api/v1/leader-board')
def display_leader_board():
    # If someone is starting the game, specialized logic for game start since a hero and dungeon need to be created.
    return jsonify(leader_board.enter()), 200


# Start the Game.
@app.route('/api/v1/start')
def start_game():
    game_token = str(uuid.uuid4())
    gamer_tag = session['gamer_tag']
    session['game_token'] = game_token  # Save game token to session.
    return jsonify(intro.start_game(gamer_tag, game_token)), 200


# Receive a blank game command... respond with a response.
@app.route('/api/v1/game/action/')
def process_no_action():
    # process action for this game.
    game_token = session['game_token']
    screen = router.process(game_token, None)
    if screen is None:
        #  Game has ended, go back to the leaderboard.
        session['game_token'] = None
        return jsonify(leader_board.enter()), 200

    # Update game_token in case the game has ended (will be None).
    session['game_token'] = screen.get('game_token')
    return jsonify(screen), 200


# Receive a game play command and respond with a json object representing each panel.
@app.route('/api/v1/game/action/<action>')
def process_action(action):
    # process action for this game.
    game_token = session['game_token']
    screen = router.process(game_token, action)
    if screen is None:
        #  Game has ended, go back to the leaderboard.
        session['game_token'] = None
        return jsonify(leader_board.enter()), 200

    return jsonify(screen), 200


if __name__ == '__main__':
    app.run()
