import random
from typing import List
from random import shuffle, randrange


def generate_dungeon_levels():
    #  loop through and create 4 dungeons, each progressively bigger
    levels = []
    last_level = False
    for level_id in range(4):
        if level_id == 3:
            last_level = True
        levels.append(make_maze(8 + level_id, 6 + level_id, level_id, last_level))

    return levels


def make_maze(w=16, h=8, dungeon_id=0, is_last=False):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["| "] * w + ['|'] for _ in range(h)] + [[]]
    ver2 = [["|   "] * w + ['|   '] for _ in range(h)] + [[]]
    hor = [["+-"] * w + ['+'] for _ in range(h + 1)]
    hor2 = [["+---"] * w + ['+   '] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+ "
                hor2[max(y, yy)][x] = "+   "
            if yy == y:
                ver[y][max(x, xx)] = "  "
                ver2[y][max(x, xx)] = "    "
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    WDL2 = '| DW'
    HDL2 = '  DW'
    if is_last:
        WDL2 = '| X '
        HDL2 = ' >< '

    # Insert the Up-Ladder and Down-Ladder
    if dungeon_id % 2 == 0:
        ver2[0][0] = '|UP '
        if ver[h - 1][w - 1] == '| ':
            ver2[h - 1][w - 1] = WDL2
        else:
            ver2[h - 1][w - 1] = HDL2
    else:
        ver2[0][0] = WDL2
        if ver[h - 1][w - 1] == '| ':
            ver2[h - 1][w - 1] = '|UP '
        else:
            ver2[h - 1][w - 1] = ' UP '

    # Add Entrances and Exits to dungeon levels
    upper_left = 'v '
    if is_last:
        upper_left = 'X '
    lower_right = '^'
    if dungeon_id % 2 == 0:
        upper_left = '^ '
        lower_right = 'v'
        if is_last:
            lower_right = 'X'
    ver[0][0] = upper_left
    ver[len(ver) - 2][len(ver[0]) - 1] = lower_right

    # Prepare the Maze and Map for Output
    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    maze: List[List[str]] = []

    buff = []
    for index in range(0, len(s)-1):
        if s[index] == '\n':
            maze.append(buff)
            buff = []
        else:
            buff.append(s[index])

    challenge_count = add_doors_traps_and_treasures(maze)
    challenge_count += add_monsters(maze)

    mmap = ""
    for (a, b) in zip(hor2, ver2):
        mmap += ''.join(a + ['\n'] + b + ['\n'])

    return {
        "maze": maze,
        "map": mmap,
        "challenge_count": challenge_count
    }


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
    # walk through every cell in the matrix.
    # Look at cells surrounding the current location: if there is only one hallway, then we have found a dead-end.
    # A pattern will always be a 7 out of 8  walls when excluding current position (i,j).

    # Loop through the 2D maze array. Start with a range of at least 1 to -2 length to avoid out-of-range errors. To
    # simplify door image combinations, using a range 1 to -3
    for y in range(1, len(maze_array) - 2):
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
                else:
                    # print("Placing Chest or Trap: x=%d, y=%d" % (x, y))
                    maze_array[y][x] = '$'
                    treasure_chest_count += 1
    return treasure_chest_count


# Randomly add traps and monsters.
def add_monsters(maze_array):
    # walk through every cell in the matrix.
    # Look empty spaces, if empty, randomly decide to put a trap or monster.
    # 10% chance for monster, 5% chance for trap.  You cannot have a trap and a monster on the same space.
    monster_count = 0
    for y in range(1, len(maze_array)-1):
        for x in range(1, len(maze_array[0])-1):
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
            position == '+' or \
            position == 'X' or \
            position == '^' or \
            position == 'v':
        return True
    return False


def is_opening(floor_space):
    return floor_space == ' '


if __name__ == "__main__":
    # Testing
    m = make_maze(10, 5, 0, True)
    print("Map: \n" + m.get("map"))
    print("Maze:")
    for row in m.get("maze"):
        print(row)
    print("Challenge Count: " + str(m.get("challenge_count")))
