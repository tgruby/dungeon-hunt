import random
from typing import List
from random import shuffle, randrange


def generate_dungeon_level(level_number):
    # limit 11 x 8 due to screen realistate
    print("Generating Level " + str(level_number))
    if level_number < 4:
        return make_maze(6 + level_number, 3 + level_number, level_number, False)
    else:
        size_adjustment = level_number % 5
        boss_level = size_adjustment == 0
        print("level: " + str(level_number) + ", mod: " + str(size_adjustment) + ", Boss: " + str(boss_level))
        return make_maze(6 + size_adjustment, 3 + size_adjustment, level_number, boss_level)


def make_maze(w=6, h=4, level_id=0, is_last=False):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["| "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+-"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+ "
            if yy == y:
                ver[y][max(x, xx)] = "  "
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    # Add Entrances and Exits to dungeon levels
    if level_id % 2 == 0:
        if not is_last:
            upper_left = 'v '
        else:
            upper_left = 'X '

        lower_right = '^ '
    else:
        upper_left = '^ '
        if not is_last:
            lower_right = 'v'
        else:
            lower_right = 'X'

    ver[0][0] = upper_left
    ver[len(ver) - 2][len(ver[0]) - 1] = lower_right

    # Prepare the Maze and Map for Output
    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    maze: List[List[str]] = []

    buff = []
    for index in range(0, len(s) - 1):
        if s[index] == '\n':
            maze.append(buff)
            buff = []
        else:
            buff.append(s[index])

    print("Level: " + str(level_id))
    traps_and_treasures = add_doors_traps_and_treasures(maze)
    treasure_count = traps_and_treasures[0]
    print("Treasure Count: " + str(treasure_count))
    trap_count = traps_and_treasures[1]
    print("Trap Count: " + str(trap_count))
    monster_count = add_monsters(maze)
    print("Monster Count: " + str(monster_count))

    return {
        "maze": maze,
        "map": create_map(maze=maze, clarivoyance=False),
        "clairvoyance_map": create_map(maze=maze, clarivoyance=True),
        "treasure_count": treasure_count,
        "treasures_collected": 0,
        "trap_count": trap_count,
        "traps_triggered": 0,
        "monster_count": monster_count,
        "monsters_killed": 0,
        "completed_challenges": [],
        "exit_door_locked": True,
        "level_completed": False
    }


def create_map(maze=None, clarivoyance=False):
    the_map = ""
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            cell = maze[y][x]
            if len(maze[0])-1 <= x+1:
                next_cell = None
            else:
                next_cell = maze[y][x+1]

            if cell == '+':
                if next_cell is None:
                    the_map += '+'
                elif next_cell == ' ':
                    the_map += '+ '
                elif next_cell == '-':
                    the_map += '+-'
                else:
                    the_map += '+ '

            if cell == '-':
                the_map += '--'
            if cell == 'v':
                the_map += '▼ '
            if cell == '^':
                the_map += '▲ '
            if cell == 'X':
                the_map += 'X '
            if cell == '|':
                the_map += '| '
            if cell == ' ':
                the_map += '  '
            if cell == 'D':
                the_map += '  '
            if cell == 'M':
                the_map += '  '
            if cell == 'T':
                if clarivoyance:
                    the_map += 'T '
                else:
                    the_map += '  '
            if cell == '$':
                if clarivoyance:
                    the_map += '$ '
                else:
                    the_map += '  '

        the_map += '\n'

    return the_map


scan_for_door = [
    [-1, -1],
    [-1, 0],
    [-1, 1],
    [0, -1],
    [0, 1],
    [1, -1],
    [1, 0],
    [1, 1]
]


# Find dead-ends and put a door in front of them, and a chest in them.  Return the count of treasure chests created.
def add_doors_traps_and_treasures(maze_array):
    treasure_chest_count = 0
    trap_count = 0
    # walk through every cell in the matrix.
    # Look at cells surrounding the current location: if there is only one hallway, then we have found a dead-end.
    # A pattern will always be a 7 out of 8  walls when excluding current position (i,j).

    # Loop through the 2D maze array. Start with a range of at least 1 to -2 length to avoid out-of-range errors. To
    # simplify door image combinations, using a range 1 to -3
    for y in range(1, len(maze_array) - 1):
        for x in range(1, len(maze_array[0]) - 1):
            opening_count = 0
            door_x = 0
            door_y = 0
            for scan in range(len(scan_for_door) - 1):
                scan_y = y + scan_for_door[scan][0]
                scan_x = x + scan_for_door[scan][1]
                if not is_wall(maze_array[scan_y][scan_x]):
                    opening_count += 1
                    door_x = scan_x
                    door_y = scan_y
            if opening_count == 1:
                # print("Placing Door: x=%d, y=%d" % (door_x, door_y))
                maze_array[door_y][door_x] = 'D'
                is_trap = random.randint(0, 3)  # 25% chance it is a trap instead of treasure
                if is_trap == 0:
                    # print("Placing Trap: x=%d, y=%d" % (x, y))
                    maze_array[y][x] = 'T'
                    trap_count += 1
                else:
                    # print("Placing Chest: x=%d, y=%d" % (x, y))
                    maze_array[y][x] = '$'
                    treasure_chest_count += 1
    return treasure_chest_count, trap_count


# Randomly add traps and monsters.
def add_monsters(maze_array):
    # walk through every cell in the matrix.
    # Look empty spaces, if empty, randomly decide to put a trap or monster.
    # 10% chance for monster, 5% chance for trap.  You cannot have a trap and a monster on the same space.
    monster_count = 0
    for y in range(1, len(maze_array) - 1):
        for x in range(1, len(maze_array[0]) - 1):
            p = maze_array[y][x]
            if is_opening(p):
                is_monster = random.randint(0, 9)
                if is_monster == 0:
                    # print("Placing Monster: x=%d, y=%d" % (x, y))
                    maze_array[y][x] = 'M'
                    monster_count += 1
                    continue
    return monster_count


def is_wall(position):
    if position == '-' or \
            position == '|' or \
            position == '+':
        return True
    return False


def is_opening(floor_space):
    return floor_space == ' '


if __name__ == "__main__":
    # Testing
    for i in range(2):
        m = generate_dungeon_level(i)
    # view = screen.paint_two_panes(
    #     hero=None,
    #     commands="Commands Goes Here",
    #     messages="Nothing to see here...",
    #     left_pane_content=images.tombstone,
    #     right_pane_content=m["map"],
    #     sound=None,
    #     delay=None,
    #     interaction_type='key_press'
    # )

        print("Map: \n" + m.get("map"))
    # for row in view.get("canvas"):
    #     print(row)

    # for row in m["maze"]:
    #     print(row)
    #
    # print(create_clarivoyance_map(m["maze"]))
