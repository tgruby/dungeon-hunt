import textwrap

medium_border = "<=====================<>====================>"
short_border = "<========<>========>"
h_border = "<=====================================<o>======================================>"
v_border = '|'
left_pane_width = 22
right_pane_width = 53
center_pane_height = 20


# Function to draw the screen given all the panel inputs
def paint(stats, commands, messages, left_pane_content, right_pane_content):
    canvas = [border("Stats"), v_border + center_text(stats, ' ', 78) + v_border, h_border]
    # Stats
    lines = create_center_pane(left_pane_content, right_pane_content)
    for line in lines:
        canvas.append(line)
    canvas.append(border("Messages"))
    # protect against too long of messages
    wrapper = textwrap.TextWrapper(width=75)
    word_list = wrapper.wrap(text=messages)
    # Print each line.
    for element in word_list:
        canvas.append(v_border + '  ' + back_padding(element, 76) + v_border)
    canvas.append(border("Commands"))
    # Commands
    canvas.append(v_border + center_text(commands, ' ', 78) + v_border)
    canvas.append(h_border)
    return canvas


# Function to build a border with a title that fits to a given length
def border(title, length=78):
    return '<' + center_text("< " + title + " >", '=', length) + '>'


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
def create_center_pane(left_image, right_image):
    if left_image is None:
        left_image = ''
    if right_image is None:
        right_image = ''

    # Left Image should be fit into a h=20, w=24 space
    left_pane_content = square_image(left_image, 20, left_pane_width)

    # Right Image should be fit into a h=20, w=47 space
    right_pane_content = square_image(right_image, 20, right_pane_width)

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
            width_cropped_image.append(line[crop:(len(line)-crop-1)])
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
    return text + padding(text, length)


def front_padding(text, length):
    return padding(text, length) + text


def padding(text, length):
    delta = length - len(text)
    buff = ''
    for x in range(delta):
        buff += ' '
    return buff


def get_stats(our_hero):
    if not our_hero.is_alive():
        return "*** YOU ARE DEAD ***"
    else:
        response = "Hit Points: %d/%d, Experience: %d, Level: %d, Gold: %d" % (
            our_hero.hit_points, our_hero.max_hit_points, our_hero.experience_points, our_hero.level, our_hero.gold)
        if our_hero.view:
            response += ", Facing: " + our_hero.view.get_direction()
        return response
