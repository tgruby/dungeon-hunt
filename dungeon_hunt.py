from flask import Flask, render_template, jsonify
import os
import view.screen
from controller import router, dungeon_design_router

# TODO: allow for multiple players playing independenty.  name+pin to login. (don't worry about security)
# TODO: Create Leaderboard (5 deep), least amount of steps to kill dragon.  Steps are counted in the dungeon.
# TODO: setup as service on Raspberry Pi


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


# Receive a command from the browser and respond with a json object representing each panel.
@app.route('/designer')
def designer():
    return render_template('designer.html')


# Receive a command from the browser and respond with a json object representing each panel.
@app.route('/designer/action/<action>')
def designer_action(action):
    return jsonify(dungeon_design_router.process(action)), 200


if __name__ == '__main__':
    app.run()
