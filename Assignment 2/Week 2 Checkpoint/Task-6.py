cleaning_space = [
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, "d", None, None, None, None, None, None, None],
    [None, None, None, None, "s", None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, "d", None, None, "l", None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, "l", None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None]
]

obstruction_space = [
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, "c", None, None, None, None, None],
    [None, None, "r", None, None, None, None, None, None, None],
    [None, None, None, None, None, None, "w", None, None, None],
    [None, None, None, None, "r", None, None, None, None, None],
    [None, "w", None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
]
"""
The context flag is used to keep track of all instances when the robot was supposed to move
forward (the instruction was forward) but ended up turning right either because it encountered a wall,
a cat or went out of bounds of the cleaning space.
"""
context = {'flag': True}
directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

"""For movement in each direction, define the displacement to be added to the
current row and current column to reach the new row and new column in the specified direction."""
displacements = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1), 'NE': (-1, 1), 'SE': (1, 1), 'SW': (1, -1),
                 'NW': (-1, -1)}


def check_for_robot(row: int, column: int) -> bool:
    """ This function checks if there is a robot at the position identified by row and column in the global
    variable obstruction_space. If there is a robot, the function returns True, else returns False.

    Parameters:
        row (int): Describes the value of the row in the obstruction space
        column (int): Describes the value of the column in the obstruction space

    Returns:
        This function returns a boolean value. If there is a robot, the function returns True, else returns False.
    """
    return obstruction_space[row][column] == 'r'


def is_within_bounds(row: int, column: int) -> bool:
    """
    This function is used to check if a value in the cleaning_space identified by a row value and column value is
    within the boundary (bounds) of the cleaning space or not. If the position identified by (row, column) is within
    the bounds of cleaning space, the function returns True, else it returns False.

    Parameters:
        row (int): Describes the value of the row in the cleaning space
        column (int): Describes the value of the column in the cleaning space

    Returns:
        This function returns a boolean value depending on whether the position identified by (row, column) is within
        the bounds of cleaning space or not.
    """
    if 0 <= row < len(cleaning_space) and 0 <= column < len(cleaning_space[0]):
        return True
    else:
        return False


def check_for_wall(row: int, column: int) -> bool:
    """
    This function checks whether there is a wall at a particular location which is identified by the value of
    (row, column) in the obstruction space. If there is a wall at that position, the function returns True, else it
    returns False.

    Parameters:
        row (int): Describes the value of the row in the obstruction space
        column (int): Describes the value of the column in the obstruction space

    Returns:
        This function returns a boolean value depending on whether there is a wall
        at the position identified by (row, column) in obstruction space.
    """
    return obstruction_space[row][column] == 'w'


def check_for_cat(row: int, column: int) -> bool:
    """
    This function checks whether there is a cat at a particular location which is identified by the value of
    (row, column) in the obstruction space. If there is a cat at that position, the function returns True, else it
    returns False.

    Parameters:
        row (int): Describes the value of the row in the obstruction space
        column (int): Describes the value of the column in the obstruction space

    Returns:
        This function returns a boolean value depending on whether there is a cat
        at the position identified by (row, column) in obstruction space.

    """
    return obstruction_space[row][column] == 'c'


def move_cat(cat_current_row, cat_current_column, row_displacement, column_displacement, vacuum):
    """
    This function is used to move the cat from its current position to a new position along the direction in which
    the vacuum is facing. The cat's current position is given by (cat_current_row,cat_current_column) in the
    obstruction space. The row_displacement, column_displacement give value which has to be added to the cat's current
    row and column respectively in order to reach its new position. If the cat can be moved to the new position, it is
    moved there and the vacuum makes a right turn. In case the cat cannot be moved, the robot just
    makes a right turn

    Parameters:
        cat_current_row (int): Indicates the current row in which the cat is present in the obstruction space
        cat_current_column (int): Indicates the current column in which the cat is present in the obstruction space
        row_displacement (int): Indicates the displacement value to be added to the cat's current row, to get the
                                cat's new row value.
        column_displacement (int): Indicates the displacement value to be added to the cat's current column, to get the
                                cat's new column value.
        Displacement value depends on the direction in which the robot is facing currently.
        vacuum(list): The vacuum list contains in order:
                                The row position of the vacuum in the space,
                                The column position of the vacuum in the space,
                                The compass facing of the vacuum from ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    Returns:
        This function does not return anything. It just updates the vacuum list.
    """
    cat_new_row = cat_current_row + row_displacement
    cat_new_column = cat_current_column + column_displacement

    # If the new position of the cat is within the bounds of cleaning space AND there is no obstruction there
    # AND there is no robot AND there is no CAT in that position already.
    if is_within_bounds(cat_new_row, cat_new_column) and obstruction_space[cat_new_row][cat_new_column] is None \
            and not check_for_wall(cat_new_row, cat_new_column) and not check_for_robot(cat_new_row, cat_new_column):
        obstruction_space[cat_new_row][cat_new_column] = 'c'
        obstruction_space[cat_current_row][cat_current_column] = None
        context['flag'] = False
        change_orientation(vacuum)

    # The cat cannot be moved to its new position since one of the above conditions were false. In this case,
    # the robot just makes a right turn.
    else:
        context['flag'] = False
        change_orientation(vacuum)


def forward(vacuum: list):
    """
        This function takes the vacuum list as input and makes the robot move forward from the current location,
        in the direction which it is facing. If the vacuum leaves the bounds of cleaning_space by moving forward,
        it performs the "turn-right" action instead.

        Parameters:
            vacuum(list): The vacuum list contains in order:
                                The row position of the vacuum in the space,
                                The column position of the vacuum in the space,
                                The compass facing of the vacuum from ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

        Returns:
            This function does not return anything. It just updates the given input vacuum list.
        """

    # Get current row, column and direction
    row, column, direction = vacuum

    # Calculate displacements based on current direction faced by robot.
    row_displacement = displacements.get(direction)[0]
    column_displacement = displacements.get(direction)[1]

    # Find the new positions of the robot
    new_row = row + row_displacement
    new_column = column + column_displacement

    # If the new position isn't within the bounds of cleaning space, make a right turn and update vacuum list in
    # change_orientation
    if not is_within_bounds(new_row, new_column):
        context['flag'] = False
        change_orientation(vacuum)
        return

    # If there is a wall at the new location, make a right turn and update vacuum list in
    # change_orientation
    if check_for_wall(new_row, new_column):
        context['flag'] = False
        change_orientation(vacuum)
        return

    # If there is a cat at the new location, make a right turn and update vacuum list in
    # change_orientation
    if check_for_cat(new_row, new_column):
        move_cat(new_row, new_column, row_displacement, column_displacement, vacuum)
        return

    # If there is a robot at the new location, make a right turn and update vacuum list in
    # change_orientation
    if check_for_robot(new_row, new_column):
        change_orientation(vacuum, "turn-left")
        return "turn-left"

    current_location = cleaning_space[row][column]
    next_location = cleaning_space[new_row][new_column]

    # Handle cases when the current location has dirt.
    if current_location == 'd':
        match next_location:
            # If next location is none, smear dirt to that location
            case None:
                cleaning_space[new_row][new_column] = 'd'

            # If next location has water, mud is set in that location
            case 'l':
                cleaning_space[new_row][new_column] = 'm'

            # If the next location has soap, None is set in that location
            case 's':
                cleaning_space[new_row][new_column] = None

    # Handle cases when the current location has either water or soap (slip and move by 2 locations
    # in its facing direction)
    elif current_location in ('l', 's'):
        # Define the row which is skipped
        skip_row, skip_column = new_row, new_column

        # The final row where the robot ends up after slipping and moving by 2 locations.
        final_row, final_column = new_row + row_displacement, new_column + column_displacement

        if is_within_bounds(final_row, final_column) and not check_for_wall(final_row, final_column):
            # Handle cases when the skipped location has a cat, wall or a robot
            if check_for_cat(skip_row, skip_column):
                move_cat(skip_row, skip_column, row_displacement, column_displacement, vacuum)
                return

            if check_for_wall(skip_row, skip_column):
                context['flag'] = False
                change_orientation(vacuum)
                return

            if check_for_robot(skip_row, skip_column):
                change_orientation(vacuum, "turn-left")
                return "turn-left"

            # Defining the position which was skipped
            skipped_position = cleaning_space[skip_row][skip_column]

            if current_location == 'l':
                match skipped_position:
                    # If skipped position had None, set 'l'(water) in that location
                    case None:
                        cleaning_space[skip_row][skip_column] = 'l'

                    # If skipped position had 'd'(dirt), set 'm' (mud) in that location
                    case 'd':
                        cleaning_space[skip_row][skip_column] = 'm'

                    # If skipped position had 's'(soap), set None in that location
                    case 's':
                        cleaning_space[skip_row][skip_column] = None

            # cleaning_space[row][column] = None
            else:
                cleaning_space[skip_row][skip_column] = None

            # Update the values of the row and column and change the obstruction space to reflect new position of
            # the robot
            vacuum[0], vacuum[1] = final_row, final_column
            obstruction_space[final_row][final_column] = 'r'
            obstruction_space[row][column] = None
            return

        # If the final row, column is not within the bounds of the cleaning space
        else:
            context['flag'] = False
            change_orientation(vacuum)
            return

    # Handle case when the current location has 'm' (mud)
    elif current_location == 'm':
        cleaning_space[new_row][new_column] = 'm'

    # Update the values of the row and column and change the obstruction space to reflect new position of
    # the robot. (Case when the robot just moves forward).
    vacuum[0], vacuum[1] = new_row, new_column
    obstruction_space[new_row][new_column] = 'r'
    obstruction_space[row][column] = None


def change_orientation(vacuum: list, command="turn-right"):
    """
        This function takes the current row and column position of the robot and changes the orientation of the robot,
        depending on the specified command.

        Parameters:
            vacuum(list): The vacuum list contains in order:
                                The row position of the vacuum in the space,
                                The column position of the vacuum in the space,
                                The compass facing of the vacuum from ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

            command(str): A string value indicating the command to be executed by the robot. The default value for this
            parameter is "turn-right" since the robot is supposed to turn right everytime it tries to leave the bounds of
            the cleaning_space by moving forward.

        Returns:
            This function does not return anything. It updates the current direction of the robot, with the new direction
            it would be facing after changing its orientation.
        """
    # When the change_orientation is called and the direction is to turn-right, execute this block
    index = directions.index(vacuum[2])
    if command == "turn-right":
        """Get the index of the current direction the vacuum is facing. The new direction will have a new index of
        current index + 1. % operator is used to handle cases when we have to move from NW to N by making a right turn"""
        new_index = (index + 1) % len(directions)
        vacuum[2] = directions[new_index]
    if command == "turn-left":
        """In this case the % operator is used to handle cases when we move from N to NW by making a left turn"""
        new_index = (index - 1) % len(directions)
        vacuum[2] = directions[new_index]


def clean(vacuum: list):
    """
               This function cleans the current position at which it is, in the cleaning_space.

               Parameters:
                   vacuum(list): The vacuum list contains in order:
                                       The row position of the vacuum in the space,
                                       The column position of the vacuum in the space,
                                       The compass facing of the vacuum from ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

               Returns:
                   This function does not return anything.
               """
    # If the current position in the cleaning space is not clean, clean it when the clean function is called
    if cleaning_space[vacuum[0]][vacuum[1]] == 'd':
        cleaning_space[vacuum[0]][vacuum[1]] = None


def vacuum_action(vacuum: list, action: str) -> str:
    """
                This function takes the vacuum list and executes the action specified in the action parameter and returns the
                action performed by the robot
                Parameters:
                vacuum(list): The vacuum list contains in order:
                                        The row position of the vacuum in the space,
                                        The column position of the vacuum in the space,
                                        The compass facing of the vacuum from ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
                action(str): A string value containing one of the following values which indicate the action to be executed:
                             forward, turn-right, turn-left, clean

                Returns:
                    This function returns the action performed by the robot

                """
    match action:
        case "forward":
            result = forward(vacuum)
            if result:
                return result
            if not context['flag']:
                context['flag'] = True
                return "turn-right"
            else:
                return "forward"
        case "turn-left":
            change_orientation(vacuum, "turn-left")
            return "turn-left"
        case "turn-right":
            change_orientation(vacuum, "turn-right")
            return "turn-right"
        case "clean":
            clean(vacuum)
            return "clean"
        case "mop":
            mop(vacuum)
            return "mop"
    return None


def mop(vacuum):
    """
        This function sets the location occupied by the vacuum in cleaning_space to None if water ("l") is at that location.

        Parameters:
                vacuum(list): The vacuum list contains in order:
                                        The row position of the vacuum in the space,
                                        The column position of the vacuum in the space,
                                        The compass facing of the vacuum from ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

        Returns:
            This function does not return anything
        """
    if cleaning_space[vacuum[0]][vacuum[1]] == 'l':
        cleaning_space[vacuum[0]][vacuum[1]] = None


def perform_cleaning(instructions, vacuums, logs):
    """
                This function reads instructions for the vacuum robot from a file and makes the robot execute those instructions.
                The actions performed by the robot are then written into the test_log file

                Parameters:
                    instructions(str): A file containing action strings on each line one after another, to be executed by the robot
                    vacuum(list): The vacuum list contains in order:
                                        The row position of the vacuum in the space,
                                        The column position of the vacuum in the space,
                                        The compass facing of the vacuum from ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
                    test_log(str): The name of the file to which the actions performed by the robot have to be written

                Returns:
                    This function  does not return anything, The actions performed by the robot are written into the test_log
                    file.
                """
    with open(instructions, 'r') as input_file:
        lines = [line.strip() for line in input_file if line.strip()]

    for log_path in logs:
        open(log_path, 'w').close()

    for line in lines:
        robot_index, actions = line.split(maxsplit=1)
        robot_index = int(robot_index)
        actions = actions.split(',')

        vacuum = vacuums[robot_index]
        log_path = logs[robot_index]

        with open(log_path, 'a') as log_file:
            for action in actions:
                result = vacuum_action(vacuum, action)
                log_file.write(result + '\n')


if __name__ == "__main__":
    test_commands = "test_commands.txt"
    test_logs = ["test_log1.txt", "test_log2.txt"]
    vacuums = [
        [2, 2, "N"],
        [4, 4, "NE"],
    ]

    print("INITIAL SPACE")
    for row_index, row in enumerate(cleaning_space):
        for col_index, cell in enumerate(row):
            if obstruction_space[row_index][col_index] is not None:
                print(obstruction_space[row_index][col_index], end='')
            elif cell is None:
                print(".", end='')
            else:
                print(cell, end='')
        print()

    print("CLEANING")
    perform_cleaning(test_commands, vacuums, test_logs)

    print("FINAL SPACE")
    for row_index, row in enumerate(cleaning_space):
        for col_index, cell in enumerate(row):
            if obstruction_space[row_index][col_index] is not None:
                print(obstruction_space[row_index][col_index], end='')
            elif cell is None:
                print(".", end='')
            else:
                print(cell, end='')
        print()

    print("ACTIONS")
    for log_file in test_logs:
        with open(log_file, "r") as log:
            print(f"FROM: {log_file}")
            print(log.read())

