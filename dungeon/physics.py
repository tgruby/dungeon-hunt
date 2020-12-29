from town import items
from dungeon import perspectives


def change_char(s, p, r):
    return s[:p] + r + s[p + 1:]


# This class is used to contain all the logic to manage the point of view of the hero as she moves through the maze.
# We use a class object here to simplify the encapsulation of the code: attributes and functions that naturally live
# together to create an "object".
class PointOfView:
    # Dungeon Map Keys
    hallway_1 = ' '
    hallway = 'H'
    wall_1 = '-'
    wall_2 = '+'
    wall_3 = '|'
    wall = 'W'
    door = 'D'
    doorway_up = '^'
    doorway_down = 'v'
    treasure = '$'
    trap = 'T'
    monstr = 'M'
    x_marks_the_spot = 'X'

    # Direction Keys
    north = 0
    east = 1
    south = 2
    west = 3

    # First Left Block by Direction: North, East, South, West
    near_left_block = [
        {"y": 0, "x": -1},
        {"y": -1, "x": 0},
        {"y": 0, "x": +1},
        {"y": +1, "x": 0}
    ]

    near_center_block = [
        {"y": 0, "x": 0},
        {"y": 0, "x": 0},
        {"y": 0, "x": 0},
        {"y": 0, "x": 0}
    ]

    near_right_block = [
        {"y": 0, "x": +1},
        {"y": +1, "x": 0},
        {"y": 0, "x": -1},
        {"y": -1, "x": 0}
    ]

    mid_left_block = [
        {"y": -1, "x": -1},
        {"y": -1, "x": +1},
        {"y": +1, "x": +1},
        {"y": +1, "x": -1}
    ]

    mid_center_block = [
        {"y": -1, "x": 0},
        {"y": 0, "x": +1},
        {"y": +1, "x": 0},
        {"y": 0, "x": -1}
    ]

    mid_right_block = [
        {"y": -1, "x": +1},
        {"y": +1, "x": +1},
        {"y": +1, "x": -1},
        {"y": -1, "x": -1}
    ]

    far_left_block = [
        {"y": -2, "x": -1},
        {"y": -1, "x": +2},
        {"y": +2, "x": +1},
        {"y": +1, "x": -2}
    ]

    far_center_block = [
        {"y": -2, "x": 0},
        {"y": 0, "x": +2},
        {"y": +2, "x": 0},
        {"y": 0, "x": -2}
    ]

    far_right_block = [
        {"y": -2, "x": +1},
        {"y": +1, "x": +2},
        {"y": +2, "x": -1},
        {"y": -1, "x": -2}
    ]

    distant_center_block = [
        {"y": -3, "x": 0},
        {"y": 0, "x": +3},
        {"y": +3, "x": 0},
        {"y": 0, "x": -3}
    ]

    blocks = [
        [near_left_block, near_center_block, near_right_block],
        [mid_left_block, mid_center_block, mid_right_block],
        [far_left_block, far_center_block, far_right_block]
    ]

    perspective_map = {
        "left_0": "a",
        "left_1": "b",
        "left_2": "c",
        "center_1": "d",
        "center_2": "e",
        "center_3": "f",
        "right_2": "g",
        "right_1": "h",
        "right_0": "i",
    }

    current_level_id = 0
    current_level = None
    current_level_map = None
    current_x = 0
    current_y = 0
    current_direction = east

    dungeon = None

    def __init__(self, game):
        self.game = game
        self.dungeon = game.dungeon
        self.set_starting_position()

    # When entering a dungeon level, we come "down" into the dungeon. We need to find the first maze we have not
    # completed, then find the up door to place our hero there. Because we either enter from the top left or bottom
    # right, we know where to begin.
    def set_starting_position(self):
        self.current_level_id = len(self.dungeon.levels)
        print("Current Level: " + str(self.current_level_id))
        self.current_level = self.dungeon.current_level["maze"]
        self.current_level_map = self.dungeon.current_level["map"]
        # Even numbers start by face east on left side of maze, odd numbers start facing west on right side
        # of maze.
        if (self.current_level_id % 2) == 0:
            self.current_direction = self.west
            self.current_y = len(self.current_level) - 2
            self.current_x = len(self.current_level[0]) - 1
        else:
            self.current_direction = self.east
            self.current_y = 1
            self.current_x = 0
        return self.step_forward()

    def generate_perspective(self):
        # Simplify variables
        d = self.current_direction
        x = self.current_x
        y = self.current_y
        # Positions should be listed in order of nearest left, nearest right, second nearest left...
        obstructions = []

        visible_limit = False

        for i, block_range in enumerate(self.blocks):
            # Ignore the Door (treat it as a Hall) if we are standing in the doorway.
            ignore_door = False
            if i == 0:
                ignore_door = True
            left_obstruction = self.get_value_at_block(d, x, y, False, block_range[0])
            center_obstruction = self.get_value_at_block(d, x, y, ignore_door, block_range[1])
            right_obstruction = self.get_value_at_block(d, x, y, False, block_range[2])

            if i != 0 and (center_obstruction == self.wall or center_obstruction == self.door):
                obstructions.append("block_" + self.perspective_map.get("center_" + str(i)) + '_' + center_obstruction)
                visible_limit = True
                break
            else:
                obstructions.append("block_" + self.perspective_map.get("left_" + str(i)) + '_' + left_obstruction)
                obstructions.append("block_" + self.perspective_map.get("right_" + str(i)) + '_' + right_obstruction)

        # If we have visibility out all 3 blocks, check to see if our end block is a hall or a wall.
        if not visible_limit:
            distant_center = self.get_value_at_block(d, x, y, False, self.distant_center_block)
            obstructions.append("block_" + self.perspective_map.get("center_" + str(3)) + '_' + distant_center)

        image_file = perspectives.build_view(obstructions)
        self.update_map()  # Don't forget to update the map
        return image_file

    # Return what we find in this block: wall, hallway, door ignoring variations
    def get_value_at_block(self, direction, x, y, ignore_door, block):
        try:
            x1 = block[direction]['x']
            y1 = block[direction]['y']
            value = self.current_level[y + y1][x + x1]
            if value == self.doorway_down or value == self.doorway_up or value == self.door:
                if ignore_door:
                    return self.hallway
                else:
                    return self.door
            if value == self.hallway_1 or \
                    value == self.x_marks_the_spot or \
                    value == self.treasure or \
                    value == self.trap or \
                    value == self.monstr:
                return self.hallway
            elif value == self.wall_1 or value == self.wall_2 or value == self.wall_3:
                return self.wall
            else:
                return value
        except IndexError:
            return self.wall

    def get_position_info(self):
        return self.current_level[self.current_y][self.current_x]

    def get_direction(self):
        if self.current_direction == self.north:
            return "North"
        if self.current_direction == self.west:
            return "West"
        if self.current_direction == self.south:
            return "South"
        if self.current_direction == self.east:
            return "East"

    def turn_left(self):
        self.current_direction = self.current_direction - 1
        if self.current_direction < 0:
            self.current_direction = 3
        return "You turned left."

    def turn_right(self):
        self.current_direction = self.current_direction + 1
        if self.current_direction > 3:
            self.current_direction = 0
        return "You turned right."

    def step_forward(self):
        x1 = self.mid_center_block[self.current_direction]['x']
        y1 = self.mid_center_block[self.current_direction]['y']
        value = self.current_level[self.current_y + y1][self.current_x + x1]

        # After you enter the dungeon, you cannot go back (unless you teleport, of course).
        if value == self.doorway_up:
            return "This door is locked."
        # If getting to the end door, and you have the key, you finish the level.
        if value == self.doorway_down:
            # Check to see if it is locked
            if self.dungeon.is_exit_door_locked():
                # Now see if we have a key, if we do, take the key, use it, and set the level to unlocked.
                if items.skeleton_key in self.game.character.inventory:
                    self.game.character.inventory.remove(items.skeleton_key)
                    self.dungeon.unlock_exit_door()
                    return "level-complete"
                else:
                    return "This door is locked."

        if value == self.hallway_1 or \
                value == self.doorway_up or \
                value == self.doorway_down or \
                value == self.door or \
                value == self.treasure or \
                value == self.trap or \
                value == self.monstr or \
                value == self.x_marks_the_spot:
            self.current_y += y1
            self.current_x += x1
            return "You move one space " + self.get_direction() + "."
        else:
            return "You can't walk through walls!"

    # Method to determine which way we need to face as we enter a new dungeon level.
    def face_forward(self):
        # You can only enter a dungeon from the left or right (east or west). That means you are standing
        # at the beginning or end of an array in the matrix.  So if you are at x position 0, you need to face east
        # otherwise, west.
        if self.current_x == 0:
            self.current_direction = self.east
        else:
            self.current_direction = self.west

    def climb_up(self):
        # First check if they are on a up_ladder
        if self.current_level[self.current_y][self.current_x] == self.doorway_up:
            # Since all previous levels have had all challenges completed, we can skip right to town.
            self.current_level_id = -1
            return
        else:
            return "You can't do that here!"

    def update_map(self):
        # First check if they are on a down_ladder
        self.current_level_map = self.dungeon.current_level["map"]
        map_array = str.splitlines(self.current_level_map)
        # Get Vertical Row (y) where we stand
        row_string = map_array[self.current_y]
        # replace our x location with an arrow.
        arrow = '↑'
        if self.current_direction == self.west:
            arrow = '←'
        elif self.current_direction == self.east:
            arrow = '→'
        elif self.current_direction == self.south:
            arrow = '↓'
        row_string = change_char(row_string, self.current_x * 2, arrow)
        map_array[self.current_y] = row_string
        new_map = ''
        for line in map_array:
            new_map += line + '\n'
        self.current_level_map = new_map
