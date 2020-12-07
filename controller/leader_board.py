import db
from view import screen, images


def enter():
    db.init_db()
    lb = db.load_leaderboard()
    response = "  Rank | Name                       | Score " + '\n'
    response += screen.medium_border + '\n'
    for i in range(len(lb.top_ten)):
        response += "   " + str(i+1) + "   | " + screen.back_padding(lb.top_ten[i].name, 26) + " | " + \
                    str(lb.top_ten[i].experience_points) + '\n'

    return screen.intro_paint(
        images.title_1,
        None,
        response,
        'Press any key to start play...',
        None,
        None
    )

