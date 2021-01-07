import textwrap

medium_border = "<----------------------o---------------------->"
short_border = "<--------o-------->"
h_border = "<--------------------------------------o--------------------------------------->"
v_border = '|'
left_pane_width = 24
right_pane_width = 51
center_pane_height = 20


# Function to draw the screen given the five panel inputs
def paint_two_panes(
        game,
        commands,
        messages,
        left_pane_content,
        right_pane_content,
        sound,
        delay,
        interaction_type
):
    canvas = [border("Stats"), v_border + center_text(get_stats(game), ' ', 78) + v_border, h_border]
    # Stats
    lines = create_center_pane(left_pane_content, right_pane_content, messages)
    for line in lines:
        canvas.append(line)

    if commands is not None:
        canvas.append(border("Commands"))
        canvas.append(v_border + center_text(commands, ' ', 78) + v_border)

    canvas.append(h_border)

    response = {
        # Updated page for the browser to paint,
        "canvas": canvas,
        # Play a sound for this screen
        "sound": sound,
        # Time to wait before allowing the player to make the next move
        "delay": delay,
        # whether the next move should happen on any key press or the enter key (key_press | enter_press)
        "interaction_type": interaction_type,
    }

    return response


# Function to draw the screen given four virt. panel inputs
def paint_one_pane(
        title_image,
        contents,
        contents_image,
        commands,
        sound,
        delay,
        animation,
        interaction_type,
        game_id
):
    canvas = []

    if title_image is not None:
        formatted_image = square_image(title_image, 5, 80)
        for line in formatted_image:
            canvas.append(line)
        canvas.append(' ')
        canvas.append(h_border)
        canvas.append(' ')

    if contents is not None:
        # Wrap long of narratives
        wrapper = textwrap.TextWrapper(width=75)
        word_list = wrapper.wrap(text=contents)
        # Print each line
        for element in word_list:
            canvas.append('   ' + back_padding(element, 80))
        canvas.append(' ')
        canvas.append(h_border)
        canvas.append(' ')

    if contents_image is not None:
        formatted_content = square_image(contents_image, 12, 70)
        for line in formatted_content:
            canvas.append(back_padding(line, 80))
        canvas.append(' ')
        canvas.append(h_border)
        canvas.append(' ')

    # command
    canvas.append(back_padding(' ', 80))
    if commands is not None:
        canvas.append(commands)

    response = {
        # Updated page for the browser to paint,
        "canvas": canvas,
        # Play a sound for this screen
        "sound": sound,
        # Time to wait before allowing the player to make the next move
        "delay": delay,
        # Whether an animation should be played
        "animation": animation,
        # whether the next move should happen on any key press or the enter key (key_press | enter_press)
        "interaction_type": interaction_type,
        "game_id": game_id
    }

    return response


# Function to build a border with a title that fits to a given length
def border(title, length=78):
    return '<' + center_text("{ " + title + " }", '-', length) + '>'


# Function to pad spacing both before and after text
def center_text(text, space, length):
    delta = length - len(text)
    delta = delta / 2
    delta -= 1  # Adjusting for rounding errors
    buff = ""
    for x in range(round(delta)):
        buff += space
    line = buff + text + buff
    # check for an off by 1 rounding error
    check = length - len(line)
    for y in range(check):
        line += space
    return line


# Create the center pane, taking the left and right image and returning an array with both together.
def create_center_pane(left_image, right_image, messages):
    if left_image is None:
        left_image = ''
    if right_image is None:
        right_image = ''

    # Left Image should be fit into a h=20, w=24 space
    left_pane_content = square_image(left_image, 20, left_pane_width)

    if messages is None:
        # Right Image should be fit into a h=20, w=47 space
        right_pane_content = square_image(right_image, 20, right_pane_width)

    else:
        wrapper = textwrap.TextWrapper(width=49)
        word_list = wrapper.wrap(text=messages)
        # Right Image should be fit into a h=20, w=47 space
        right_pane_content = square_image(right_image, 20-(len(word_list)+1), right_pane_width)
        right_pane_content.append('---------------------{ Info }----------------------')
        # protect against too long of messages
        # Print each line.
        for element in word_list:
            right_pane_content.append(' ' + back_padding(element, 49) + ' ')

    # Put the images together
    buff = []
    for index in range(20):
        buff.append(' ' + v_border + left_pane_content[index] +
                    v_border + right_pane_content[index] + v_border)

    return buff


# Images are irregular shapes.  We need to make every line the same length, crop them, and center them.
def square_image(image, height, width):
    if image is None:
        image = ''

    # Break Image into an array of strings
    image_lines = str.splitlines(image)
    # First box the image, then crop it, then center it.
    boxed_image = box_image(image_lines)

    cropped_image = crop_image(boxed_image, height, width)

    centered_image = []
    for image in cropped_image:
        centered_image.append(center_text(image, ' ', width))

    return centered_image


# Function to make all lines the same size, this will help with positioning
def box_image(image):
    # Find the longest line
    longest_line = 0
    for line in image:
        if len(line) > longest_line:
            longest_line = len(line)

    # Buffer all the lines
    new_image = []
    for line in image:
        new_image.append(back_padding(line, longest_line))

    return new_image


# Function to crop an image to the given height and width
def crop_image(image, height, width):
    # Crop the height.  Height Cropping should just cut off the bottom of the image
    height_cropped_image = []
    if len(image) > height:
        for index in range(height):
            height_cropped_image.append(image[index])
    # Image height is too short, lengthen it with white space
    elif len(image) < height:
        delta = height - len(image)
        half = delta / 2
        height_cropped_image = image
        for index in range(delta):
            if index < half:
                if not height_cropped_image:
                    height_cropped_image.append(back_padding(' ', 1))
                else:
                    height_cropped_image.insert(0, back_padding(' ', len(height_cropped_image[0])))
            else:
                height_cropped_image.append(back_padding(' ', len(height_cropped_image[0])))
    else:
        height_cropped_image = image

    # Crop width by cropping from the center
    width_cropped_image = []
    if len(height_cropped_image[0]) > width:
        delta = len(height_cropped_image[0]) - width
        crop = round(delta / 2)
        for line in height_cropped_image:
            width_cropped_image.append(line[crop:(len(line) - crop - 1)])
    else:
        width_cropped_image = height_cropped_image

    return width_cropped_image


def list_inventory(our_hero):
    response = border("Equipped Items", 43) + '\n'
    response += "    Weapon..... %s (%d)\n" % (our_hero.equipped_weapon['name'], our_hero.equipped_weapon['damage'])
    if our_hero.equipped_armor is not None:
        response += "    Armor...... %s (%d)\n" % (our_hero.equipped_armor['name'], our_hero.equipped_armor['damage'])
    if our_hero.equipped_shield is not None:
        response += "    Shield..... %s (%d)\n" % (our_hero.equipped_shield['name'], our_hero.equipped_shield['damage'])
    response += border("Inventory", 43) + '\n'

    collapsed_items = collapse_inventory_items(our_hero)

    # List the items on the screen
    for num, i in enumerate(collapsed_items):
        response += "    %d. %d %s" % (num + 1, i[0], i[1])
        response += '\n'
    return response


def collapse_inventory_items(our_hero):
    # Create Collections for each item (and count up the number of each that we have):
    collapsed_items = []
    for item in our_hero.inventory:
        item_found = False
        for collapsed_item in collapsed_items:
            if collapsed_item[1] == item["name"]:
                collapsed_item[0] += 1  # Increment Count
                item_found = True
        if not item_found:
            # Format of list items are: count, name, type, value, item
            collapsed_item = [1, item["name"], item["type"], item["cost"], item]
            collapsed_items.append(collapsed_item)

    return collapsed_items


def back_padding(text, length):
    pad = text + padding(text, length)
    if len(pad) > length:
        pad = pad[:length]
    return pad


def front_padding(text, length):
    pad = padding(text, length) + text
    if len(pad) > length:
        pad = pad[:length]
    return pad


def padding(text, length):
    delta = length - len(text)
    buff = ''
    for x in range(delta):
        buff += ' '
    return buff


def get_stats(game):
    level = game.dungeon.current_level_id
    if level == 0:
        level = 1  # For display purposes, just show 1 at the start.
    if game is None:
        return "*** NO STATS INFO ***"
    if not game.character.is_alive():
        return "*** YOU ARE DEAD ***"
    else:
        hero = game.character
        response = "HP: %d/%d, Level: %d, Gold: %d, Score: %d" % (
            hero.hit_points, hero.max_hit_points, level, hero.gold, game.score)
        if hero.view:
            response += ", Facing: " + hero.view.get_direction()
        return response
