cleaning_space = [
    [None, None, None, None, None, None, None, None, None, None],
    [None, None, "d", None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
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
    [None, None, None, None, None, None, None, None, None, None],
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


def is_within_bounds(row: int, column: int) -> bool:
    """
    This function checks whether a point in the cleaning space identified by (row, column) is within the bounds of the
    cleaning space or not. If the point is within the cleaning space, the function returns True, else it returns False.

    Parameters:
        row(int): An integer value representing the row position in the cleaning space
        column(int): An integer value representing the column position in the cleaning space

    Returns:
        This function returns a boolean value which indicates whether the particular point identified by (row, column)
        in the cleaning space is within the bounds of the cleaning space or not.
    """
    if 0 <= row < len(cleaning_space) and 0 <= column < len(cleaning_space[0]):
        return True
    else:
        return False


def check_for_cat(row, column):
    """
    This is a helper function which checks if a cat is present in the cleaning space at the position identified by
    (row, column). If a cat is present in the cleaning space at the position identified by (row, column), the function
    returns True, else it returns False

    Parameters:
        row(int): An integer value representing the row position in the cleaning space
        column(int): An integer value representing the column position in the cleaning space

    Returns:
        This function returns a boolean value which indicates whether the particular point identified by (row, column)
        in the cleaning space has a cat in that point or not. If cat is present at that point, it returns True, else
        it returns False.
    """
    return obstruction_space[row][column] == 'c'


def move_cat(cat_current_row, cat_current_column, row_displacement, column_displacement, vacuum):
    """
    This is a helper function which is used to move a cat from its current location to a new location in the obstruction
    space. The cat is moved in the direction which is faced by the robot. If by moving the cat, it goes out of bounds,
    the cat is not moved and the robot just makes a right turn. If the cat can be successfully moved, the cat is moved
    and the robot makes a right turn.

    Parameters:
        cat_current_row(int): The cat's current row position in the obstruction space.
        cat_current_column(int): The cat's current column position in the obstruction space
        row_displacement(int): An integer value representing the row displacement to be added to the cat's current row
                               so that the cat reaches its new position. This is calculated depending on the current
                               direction faced by the robot.
        column_displacement(int): An integer value representing the column displacement to be added to the cat's current
                                column so that the cat reaches its new position. This is calculated depending on
                                the current direction faced by the robot.
        vacuum(list): The vacuum list contains in order:
                                The row position of the vacuum in the space,
                                The column position of the vacuum in the space,
                                The compass facing of the vacuum from ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    """
    # Calculating the new row and new column position for the cat
    cat_new_row = cat_current_row + row_displacement
    cat_new_column = cat_current_column + column_displacement

    # Execute this block if the cat's new row and new column position is within the bounds of the obstruction place.
    if is_within_bounds(cat_new_row, cat_new_column) and obstruction_space[cat_new_row][cat_new_column] is None:
        obstruction_space[cat_new_row][cat_new_column] = 'c'
        obstruction_space[cat_current_row][cat_current_column] = None
        change_orientation(vacuum)
        context['flag'] = False

    # Execute this block if the cat's new row and new column position is not within the bounds of the obstruction place.
    else:
        change_orientation(vacuum)
        context['flag'] = False


def forward(vacuum: list):
    """
        This function takes the vacuum list as input and makes the robot move forward from the current location,
        in the direction which it is facing. If the vacuum leaves the bounds of cleaning_space or encounters a wall by
        moving forward, it performs the "turn-right" action instead. If the vacuum overlaps with a cat ("c") by
        moving forward, the cat will move by one location in the direction of the vacuum's facing if the space is clear
        of obstructions; and the vacuum performs the "turn-right" action instead.

            Parameters:
                vacuum(list): The vacuum list contains in order:
                                    The row position of the vacuum in the space,
                                    The column position of the vacuum in the space,
                                    The compass facing of the vacuum from ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

            Returns:
                This function does not return anything. It just updates the given input vacuum list.
            """
    total_rows, total_columns = len(cleaning_space), len(cleaning_space[0])
    row, column, direction = vacuum

    # Calculate the row and column displacements for the forward movement.
    row_displacement = displacements.get(direction)[0]
    column_displacement = displacements.get(direction)[1]

    # Calculate the new row and new column values for the forward movement of the robot
    new_row = row + row_displacement
    new_column = column + column_displacement

    """If the new position of the robot after considering the forward movement is within the bounds of the cleaning space, 
    execute this block"""
    if is_within_bounds(new_row, new_column):
        # If the new position has a wall at that position
        if obstruction_space[new_row][new_column] == 'w':
            context['flag'] = False
            change_orientation(vacuum)
            return

        # If the new position has a cat at that position
        if check_for_cat(new_row, new_column):
            move_cat(new_row, new_column, row_displacement, column_displacement, vacuum)
            return

        # If the current position has dirt at that position execute this block of code.
        if cleaning_space[row][column] == 'd':
            # If the new position has no dirt, smear dirt into that location
            if cleaning_space[new_row][new_column] is None:
                cleaning_space[new_row][new_column] = 'd'
            # If the new position has water in that location, set mud 'm' in that location
            elif cleaning_space[new_row][new_column] == 'l':
                cleaning_space[new_row][new_column] = 'm'

        # If the current position has water in that location execute this block of code.
        elif cleaning_space[row][column] == 'l':
            """
            Calculate the final_row, final_displacement where the robot would end up after slipping and moving
            by two locations.
            """
            final_row = new_row + row_displacement
            final_column = new_column + column_displacement

            # If the final position of the vacuum is within the bounds of the cleaning space, execute this block of code
            if is_within_bounds(final_row, final_column):
                # If the vacuum skips over a clean (None) location, water ("l") is set in the location it skipped over.
                if cleaning_space[new_row][new_column] is None:
                    cleaning_space[new_row][new_column] = 'l'
                # If the vacuum skips over a dirt ("d") location, mud ("m") is set in the location it skipped over.
                elif cleaning_space[new_row][new_column] == 'd':
                    cleaning_space[new_row][new_column] = 'm'

                # Check if cat is present in the position which the robot skips
                if check_for_cat(new_row, new_column):
                    move_cat(new_row, new_column, row_displacement, column_displacement, vacuum)
                    return

                # Check if wall is present in the position which the robot skips
                if obstruction_space[new_row][new_column] == 'w':
                    change_orientation(vacuum)
                    context['flag'] = False
                    return

                # Update the final position for row and column in the vacuum list.
                vacuum[0] = final_row
                vacuum[1] = final_column
                # Make changes in the obstruction_space to reflect the new position of the robot
                obstruction_space[row][column] = None
                obstruction_space[final_row][final_column] = 'r'
                return

            else:
                """If the final position of the vacuum is NOT within the bounds of the cleaning space, 
                execute this block of code"""
                change_orientation(vacuum)
                context['flag'] = False

        elif cleaning_space[row][column] == 'm':
            """If the vacuum is over a location with mud ("m") in cleaning_space when it performs the "forward" 
            action, it will move by one location and smear the mud into the location it ends in after the action. Mud 
            ("m") is set in its new location. """
            cleaning_space[new_row][new_column] = 'm'

        else:
            """If none of the above conditions are met, the robot just moves forward. In that case, update the new 
            row and new column positions of the robot in the vacuum list and make changes in the obstruction_space to 
            reflect the new position of the robot """
            vacuum[0] = new_row
            vacuum[1] = new_column
            obstruction_space[row][column] = None
            obstruction_space[new_row][new_column] = 'r'

    else:
        """Execute this block if the robot's new position identified by (new_row, new_column) is out of bounds 
        of the cleaning space."""
        context['flag'] = False
        change_orientation(vacuum)


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

    if command == "turn-right":
        """Get the index of the current direction the vacuum is facing. The new direction will have a new index of
        current index + 1. % operator is used to handle cases when we have to move from NW to N by making a right turn"""
        index = directions.index(vacuum[2])
        new_index = (index + 1) % len(directions)
        vacuum[2] = directions[new_index]

    if command == "turn-left":
        """In this case the % operator is used to handle cases when we move from N to NW by making a left turn"""
        index = directions.index(vacuum[2])
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
            forward(vacuum)
            if not context['flag']:
                context['flag'] = True
                return "turn-right"
            else:
                return "forward"
        case "turn-left":
            change_orientation(vacuum, action)
            return "turn-left"
        case "turn-right":
            change_orientation(vacuum, action)
            return "turn-right"
        case "clean":
            clean(vacuum)
            return "clean"
        case "mop":
            mop(vacuum)
            return "mop"


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


def perform_cleaning(instructions: str, vacuum: list, test_log: str):
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
        with open(test_log, 'w') as log_file:
            lines = input_file.readlines()
            for index in range(len(lines)):
                lines[index] = lines[index].strip()
            for index, action in enumerate(lines):
                action_performed = vacuum_action(vacuum, action)
                log_file.write(action_performed + '\n')


if __name__ == "__main__":
    test_commands = "test_commands.txt"
    test_log = "test_log.txt"
    vacuum = [1, 1, "W"]
    print("INITIAL SPACE")
    for row_index, row in enumerate(cleaning_space):
        for col_index, cell in enumerate(row):
            if obstruction_space[row_index][col_index] is not None:
                print(obstruction_space[row_index][col_index], end='')
            elif cell:
                print(".", end='')
            else:
                print("d", end='')
        print()
    print("CLEANING")
    perform_cleaning(test_commands, vacuum, test_log)
    print("FINAL SPACE")
    for row_index, row in enumerate(cleaning_space):
        for col_index, cell in enumerate(row):
            if obstruction_space[row_index][col_index] is not None:
                print(obstruction_space[row_index][col_index], end='')
            elif cell:
                print(".", end='')
            else:
                print("d", end='')
        print()
    print(vacuum)
    print("ACTIONS")
    with open(test_log, "r") as log:
        print(log.read())

