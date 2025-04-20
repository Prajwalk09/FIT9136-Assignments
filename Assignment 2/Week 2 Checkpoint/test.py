cleaning_space = [[True, True, True], [True, True, True], [True, True, True]]
directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
displacements = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1), 'NE': (-1, 1), 'SE': (1, 1), 'SW': (1, -1),
                 'NW': (-1, -1)}


def forward(vacuum):
    total_rows, total_columns = len(cleaning_space), len(cleaning_space[0])
    row, column, direction = vacuum
    row_displacement = displacements.get(direction)[0]
    column_displacement = displacements.get(direction)[1]

    new_row = row + row_displacement
    new_column = column + column_displacement

    if not (0 < new_row < total_rows and 0 < new_column < total_columns):
        change_orientation(vacuum)

    else:
        if not cleaning_space[row][column]:
            cleaning_space[new_row][new_column] = False

    vacuum[0] = new_row
    vacuum[1] = new_column
    print(new_row, new_column)


def change_orientation(vacuum, command="turn-right"):
    if command == "turn-right":
        index = directions.index(vacuum[2])
        new_index = (index + 1) % len(directions)
        vacuum[2] = directions[new_index]

    if command == "turn-left":
        index = directions.index(vacuum[2])
        new_index = (index - 1) % len(directions)
        vacuum[2] = directions[new_index]


def clean(vacuum):
    if not cleaning_space[vacuum[0]][vacuum[1]]:
        cleaning_space[vacuum[0]][vacuum[1]] = True


def vacuum_action(vacuum, action):
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
    with open(instructions, 'r') as input_file:
        lines = input_file.readlines()
        for index in range(len(lines)):
            lines[index] = lines[index].strip()

        for index, action in enumerate(lines):
            vacuum_action(vacuum, action)


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    test_commands = "test_commands.txt"
    vacuum = [1, 1, "N"]

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
