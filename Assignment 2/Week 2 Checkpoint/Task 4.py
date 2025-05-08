cleaning_space = [
    [True,True,True ,True,True ,True ,True,True,True,True],
    [True,True,False,True,True ,True ,True,True,True,True],
    #          ^^^^^
    [True,True,True ,True,True ,True ,True,True,True,True],
    [True,True,True ,True,True ,True ,True,True,True,True],
    [True,True,False,True,True ,False,True,True,True,True],
    #          ^^^^^            ^^^^^
    [True,True,True ,True,True ,True ,True,True,True,True],
    [True,True,True ,True,False,True ,True,True,True,True],
    #                     ^^^^^
    [True,True,True ,True,True ,True ,True,True,True,True],
    [True,True,True ,True,True ,True ,True,True,True,True],
    [True,True,True ,True,True ,True ,True,True,True,True]
    ]

obstruction_space = [
    [None,None,None,None,None,None,None,None,None,None],
    [None,None,None,None,"c" ,None,None,None,None,None],
    [None,None,"r" ,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,"w" ,None,None,None],
    [None,None,None,None,None,None,None,None,None,None],
    [None,"w" ,None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None,None,None],
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
    # Get current row, column and direction
    row, column, direction = vacuum

    # Get the row and column displacements to be added for the current direction
    row_displacement = displacements.get(direction)[0]
    column_displacement = displacements.get(direction)[1]

    new_row = row + row_displacement
    new_column = column + column_displacement

    # Checking if new row and new column are within the bounds of the cleaning space
    if 0 <= new_row < total_rows and 0 <= new_column < total_columns:
        # If robot encounters a wall by moving forward, set the flag to False, turn right and don't execute further
        if obstruction_space[new_row][new_column] == 'w':
            context['flag'] = False
            change_orientation(vacuum)
            return

        # If the robot encounters a cat by moving forward, execute this block
        if obstruction_space[new_row][new_column] == 'c':
            cat_current_row, cat_current_column = new_row, new_column

            # Finding the new row and new column positions for the cat, in the current direction
            cat_new_row = cat_current_row + row_displacement
            cat_new_column = cat_current_column + column_displacement

            # Checking if the cat's new positions are within bounds
            if (0 <= cat_new_row < total_rows and 0 <= cat_new_column < total_columns) and \
                    obstruction_space[cat_new_row][cat_new_column] is None:
                # Update cat's current position with None and move it to new position, change orientation of robot
                # after that
                obstruction_space[cat_new_row][cat_new_column] = 'c'
                obstruction_space[cat_current_row][cat_current_column] = None
                context['flag'] = False
                change_orientation(vacuum)
                return

            # If cat's new position not within bounds, the robot just turns right and cat stays where it is
            else:
                context['flag'] = False
                change_orientation(vacuum)
                return

        # If the robot does not encounter a wall or a cat, then it is supposed to just move forward
        # Update the new row and new column position of the robot
        vacuum[0] = new_row
        vacuum[1] = new_column
        # Update the obstruction space with the robot's new position
        obstruction_space[row][column] = None
        obstruction_space[new_row][new_column] = 'r'

        # If the current position is not clean, robot smears the dirt to the new location
        if not cleaning_space[row][column]:
            cleaning_space[new_row][new_column] = False

    # When the robot's new row and new column position end up being outside the bounds of the cleaning space,
    # set the flag to false and make a right turn
    else:
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
    if not cleaning_space[vacuum[0]][vacuum[1]]:
        cleaning_space[vacuum[0]][vacuum[1]] = True


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
                # If the flag is false, the robot made a right turn when it was supposed to move forward
                # Set the flag to true for next iterations, and return turn-right
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
                # Getting rid of the \n character at the end of each line of the file
                lines[index] = lines[index].strip()

            # For each action in the file, make the vacuum perform that action and log the action performed to the
            # test_log file
            for index, action in enumerate(lines):
                action_performed = vacuum_action(vacuum, action)
                log_file.write(action_performed + '\n')



# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    test_commands = "test_commands.txt"
    test_log = "test_log.txt"
    vacuum = [2,2,"N"]

    print("INITIAL SPACE")
    for row_index,row in enumerate(cleaning_space):
        for col_index,cell in enumerate(row):
            if obstruction_space[row_index][col_index] is not None:
                print(obstruction_space[row_index][col_index],end='')
            elif cell:
                print(".",end='')
            else:
                print("d",end='')
        print()

    print("CLEANING")
    perform_cleaning(test_commands,vacuum,test_log)

    print("FINAL SPACE")
    for row_index,row in enumerate(cleaning_space):
        for col_index,cell in enumerate(row):
            if obstruction_space[row_index][col_index] is not None:
                print(obstruction_space[row_index][col_index],end='')
            elif cell:
                print(".",end='')
            else:
                print("d",end='')
        print()

    print("ACTIONS")
    with open(test_log,"r") as log:
        print(log.read())
