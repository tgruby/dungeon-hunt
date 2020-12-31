import sys
from game_play import db


if __name__ == '__main__':
    command = sys.argv[1]
    lb = db.load_leaderboard()

    if command == 'delete':
        leader_no = int(sys.argv[2])
        print("Deleting: " + str(lb.leaders[leader_no].character.name))
        del lb.leaders[leader_no]
        print("LB Entry Deleted.")
        db.save_leaderboard(lb)
    if command == "list":
        for idx, game in enumerate(lb.leaders):
            print("Index:" + str(idx) + ", Name: " + game.character.name + ", Score:" + str(game.score) + ", Game ID: " + game.game_id)
