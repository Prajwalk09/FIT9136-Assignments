cleaning_space = [
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, False, True, True, True, True, True, True, True],
    #          ^^^^^
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, False, True, True, False, True, True, True, True],
    #          ^^^^^           ^^^^^
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, False, True, True, True, True, True],
    #                    ^^^^^
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True]
]
# Defining directions in which the vacuum can be facing
directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']


def forward(vacuum):
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
    row, column, direction = vacuum
    match direction:
        case "N":
            """Robot is facing North and it has to move forward. If it is anywhere in the first row, it does not have 
            anywhere to go ahead. Hence make a right turn."""
            if row == 0:
                change_orientation(vacuum)
            else:
                """If the vacuum is over a dirty location in cleaning_space when it performs the "forward" action, 
                it will smear the dirt into the location it ends in after the action and set its new location in 
                cleaning_space to False."""
                if not cleaning_space[row][column]:
                    cleaning_space[row - 1][column] = False
                # Update the new position of the robot's row
                vacuum[0] -= 1

        case "S":
            """Robot is facing South and it has to move forward. If it is anywhere in the last row, it does not have 
            anywhere to go ahead. Hence make a right turn."""
            if row + 1 == len(cleaning_space):
                change_orientation(vacuum)
            else:
                """If the vacuum is over a dirty location in cleaning_space when it performs the "forward" action, 
                it will smear the dirt into the location it ends in after the action and set its new location in 
                cleaning_space to False."""
                if not cleaning_space[row][column]:
                    cleaning_space[row + 1][column] = False
                # Update the new position of the robot's row
                vacuum[0] += 1

        case "E":
            """Robot is facing East and it has to move forward. If it is anywhere in the last column, it does not 
            have anywhere to go ahead. Hence make a right turn."""
            if column + 1 == len(cleaning_space):
                change_orientation(vacuum)
            else:
                """If the vacuum is over a dirty location in cleaning_space when it performs the "forward" action, 
                it will smear the dirt into the location it ends in after the action and set its new location in 
                cleaning_space to False."""
                if not cleaning_space[vacuum[0]][vacuum[1]]:
                    cleaning_space[row][column + 1] = False
                # Update the new position of the robot's column
                vacuum[1] += 1

        case "W":
            """Robot is facing West and it has to move forward. If it is anywhere in the first column, it does not 
            have anywhere to go ahead. Hence make a right turn."""
            if column - 1 < 0:
                change_orientation(vacuum)
            else:
                """If the vacuum is over a dirty location in cleaning_space when it performs the "forward" action, 
                it will smear the dirt into the location it ends in after the action and set its new location in 
                cleaning_space to False."""
                if not cleaning_space[row][column]:
                    cleaning_space[row][column - 1] = False
                # Update the new position of the robot's column
                vacuum[1] -= 1

        case "NE":
            """Robot is facing North East and it has to move forward. If it is anywhere in the first row or last 
            column, it does not have anywhere to go ahead. Hence make a right turn."""
            if row == 0 or column == len(cleaning_space) - 1:
                change_orientation(vacuum)
            else:
                """If the vacuum is over a dirty location in cleaning_space when it performs the "forward" action, 
                it will smear the dirt into the location it ends in after the action and set its new location in 
                cleaning_space to False."""
                if not cleaning_space[row][column]:
                    cleaning_space[row - 1][column + 1] = False
                # Update the new position of the robot's row and column
                vacuum[0] -= 1
                vacuum[1] += 1

        case "NW":
            """Robot is facing North West and it has to move forward. If it is anywhere in the first row or first 
            column, it does not have anywhere to go ahead. Hence make a right turn."""
            if row == 0 or column == 0:
                change_orientation(vacuum)
            else:
                """If the vacuum is over a dirty location in cleaning_space when it performs the "forward" action, 
                it will smear the dirt into the location it ends in after the action and set its new location in 
                cleaning_space to False."""
                if not cleaning_space[row][column]:
                    cleaning_space[row - 1][column - 1] = False
                # Update the new position of the robot's row and column
                vacuum[0] -= 1
                vacuum[1] -= 1

        case "SE":
            """Robot is facing South East and it has to move forward. If it is anywhere in the last row or last 
            column, it does not have anywhere to go ahead. Hence make a right turn."""
            if vacuum[0] == len(cleaning_space) - 1 or vacuum[1] == len(cleaning_space) - 1:
                change_orientation(vacuum)
            else:
                """If the vacuum is over a dirty location in cleaning_space when it performs the "forward" action, 
                it will smear the dirt into the location it ends in after the action and set its new location in 
                cleaning_space to False."""
                if not cleaning_space[row][column]:
                    cleaning_space[row + 1][column + 1] = False
                # Update the new position of the robot's row and column
                vacuum[0] += 1
                vacuum[1] += 1

        case "SW":
            """Robot is facing South West and it has to move forward. If it is anywhere in the last row or first 
            column, it does not have anywhere to go ahead. Hence make a right turn."""
            if row == len(cleaning_space) - 1 or column == 0:
                change_orientation(vacuum)
            else:
                """If the vacuum is over a dirty location in cleaning_space when it performs the "forward" action, 
                it will smear the dirt into the location it ends in after the action and set its new location in 
                cleaning_space to False."""
                if not cleaning_space[row][column]:
                    cleaning_space[row + 1][column - 1] = False
                # Update the new position of the robot's row and column
                vacuum[0] += 1
                vacuum[1] -= 1


def change_orientation(vacuum, command="turn-right"):
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
    if command == "turn-right":
        """
        Get the index of the current direction the vacuum is facing. The new direction will have a new index of
        current index + 1. % operator is used to handle cases when we have to move from NW to N by making a right turn
        """
        index = directions.index(vacuum[2])
        new_index = (index + 1) % len(directions)
        vacuum[2] = directions[new_index]

    if command == "turn-left":
        """
        In this case the % operator is used to handle cases when we move from N to NW by making a left turn
        """
        index = directions.index(vacuum[2])
        new_index = (index - 1) % len(directions)
        vacuum[2] = directions[new_index]


def clean(vacuum):
    """
    This function cleans the current position at which it is, in the cleaning_space.

    Parameters:
        vacuum(list): The vacuum list contains in order:
                            The row position of the vacuum in the space,
                            The column position of the vacuum in the space,
                            The compass facing of the vacuum from ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


    """
    # If the current position in the cleaning space is not clean, clean it when the clean function is called
    if not cleaning_space[vacuum[0]][vacuum[1]]:
        cleaning_space[vacuum[0]][vacuum[1]] = True


def vacuum_action(vacuum, action):
    """
    This function takes the vacuum list and executes the action specified in the action parameter.

    Parameters:
    vacuum(list): The vacuum list contains in order:
                            The row position of the vacuum in the space,
                            The column position of the vacuum in the space,
                            The compass facing of the vacuum from ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    action(str): A string value containing one of the following values which indicate the action to be executed:
                 forward, turn-right, turn-left, clean

    Returns:
        This function does not return anything. Depending on the action specified, it calls the corresponding function

    """
    # Depending on the action specified, make the vacuum perform the corresponding action
    match action:
        case "forward":
            forward(vacuum)
        case "turn-left":
            change_orientation(vacuum, action)
        case "turn-right":
            change_orientation(vacuum, action)
        case "clean":
            clean(vacuum)


def perform_cleaning(instructions, vacuum):
    """
    This function reads instructions for the vacuum robot from a file and makes the robot execute those instructions.

    Parameters:
        instructions(str): A file containing action strings on each line one after another, to be executed by the robot
        vacuum(list): The vacuum list contains in order:
                            The row position of the vacuum in the space,
                            The column position of the vacuum in the space,
                            The compass facing of the vacuum from ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    Returns:
        This function  does not return anything, the contents of the vacuum list and the cleaning_space
        locations are updated.

    """
    # Opening and reading the commands from the instructions file
    with open(instructions, 'r') as input_file:
        lines = input_file.readlines()
        for index in range(len(lines)):
            # Getting rid of the \n character at the end of each line of the file
            lines[index] = lines[index].strip()

        # For each action in the file, make the vacuum perform that action
        for index, action in enumerate(lines):
            vacuum_action(vacuum, action)


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    test_commands = "test_commands.txt"
    vacuum = [2, 2, "N"]

    print("INITIAL SPACE")
    for row_index, row in enumerate(cleaning_space):
        for col_index, cell in enumerate(row):
            if (row_index, col_index) == (vacuum[0], vacuum[1]):
                print("r", end='')
            elif cell:
                print(".", end='')
            else:
                print("d", end='')
        print()

    print("CLEANING")
    perform_cleaning(test_commands, vacuum)

    print("FINAL SPACE")
    for row_index, row in enumerate(cleaning_space):
        for col_index, cell in enumerate(row):
            if (row_index, col_index) == (vacuum[0], vacuum[1]):
                print("r", end='')
            elif cell:
                print(".", end='')
            else:
                print("d", end='')
        print()
