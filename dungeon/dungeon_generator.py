import random
from game_play import screen, images
from typing import List
from random import shuffle, randrange
#
# dungeon_levels = [
#     {"width": 6, "height": 3, "monsters": monsters.l1_list, "boss_level": False},
#     {"width": 6, "height": 3, "monsters": monsters.l1_list, "boss_level": False},
#     {"width": 6, "height": 3, "monsters": monsters.l1_list, "boss_level": False}
# ]


def generate_dungeon_level(level_number):
    # limit 11 x 8 due to screen realistate
    # boss_level = False
    if level_number == 4 or level_number == 9 or level_number == 14:
        boss_level = True
    if level_number > 4:
        size_adjustment = level_number % 5
        print("mod: " + str(size_adjustment))
        return make_maze(7 + size_adjustment, 4 + size_adjustment, level_number, False)
    else:
        return make_maze(7 + level_number, 4 + level_number, level_number, False)


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

    wdl2 = '| ▼ '
    hdl2: str = '  ▼ '
    if is_last:
        wdl2 = '| ╳ '
        hdl2 = '  ╳ '

    # Insert the Up-Door and Down Door
    if dungeon_id % 2 == 0:
        ver2[0][0] = '| ▲ '
        if ver[h - 1][w - 1] == '| ':
            ver2[h - 1][w - 1] = wdl2
        else:
            ver2[h - 1][w - 1] = hdl2
    else:
        ver2[0][0] = wdl2
        if ver[h - 1][w - 1] == '| ':
            ver2[h - 1][w - 1] = '| ▲ '
        else:
            ver2[h - 1][w - 1] = '  ▲ '

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
    for index in range(0, len(s) - 1):
        if s[index] == '\n':
            maze.append(buff)
            buff = []
        else:
            buff.append(s[index])

    print("Level: " + str(dungeon_id))
    traps_and_treasures = add_doors_traps_and_treasures(maze)
    treasure_count = traps_and_treasures[0]
    print("Treasure Count: " + str(treasure_count))
    trap_count = traps_and_treasures[1]
    print("Trap Count: " + str(trap_count))
    monster_count = add_monsters(maze)
    print("Monster Count: " + str(monster_count))

    mmap = ""
    for (a, b) in zip(hor2, ver2):
        mmap += ''.join(a + ['\n'] + b + ['\n'])

    return {
        "maze": maze,
        "map": mmap,
        "clairvoyance_map": create_clarivoyance_map(maze),
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


def create_clarivoyance_map(maze):
    all_map = ""
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            cell = maze[y][x]
            if len(maze[0])-1 <= x+1:
                next_cell = None
            else:
                next_cell = maze[y][x+1]

            if cell == '+':
                if next_cell is None:
                    all_map += '+'
                elif next_cell == ' ':
                    all_map += '+ '
                elif next_cell == '-':
                    all_map += '+-'
                else:
                    all_map += '+ '

            if cell == '-':
                all_map += '--'
            if cell == 'v':
                all_map += '▼ '
            if cell == '^':
                all_map += '▲ '
            if cell == '|':
                all_map += '| '
            if cell == ' ':
                all_map += '  '
            if cell == 'D':
                all_map += '  '
            if cell == 'M':
                all_map += 'M '
            if cell == 'T':
                all_map += 'T '
            if cell == '$':
                all_map += '$ '

        all_map += '\n'

    return all_map


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
    m = generate_dungeon_level(9)
    view = screen.paint_two_panes(
        hero=None,
        commands="Commands Goes Here",
        messages="Nothing to see here...",
        left_pane_content=images.tombstone,
        right_pane_content=m["map"],
        sound=None,
        delay=None,
        interaction_type='key_press'
    )

    print("Map: \n" + m.get("map"))
    for row in view.get("canvas"):
        print(row)

    for row in m["maze"]:
        print(row)

    print(create_clarivoyance_map(m["maze"]))
