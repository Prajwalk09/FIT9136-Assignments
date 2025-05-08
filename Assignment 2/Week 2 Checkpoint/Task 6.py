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
context = {'flag': True}
directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

displacements = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1), 'NE': (-1, 1), 'SE': (1, 1), 'SW': (1, -1),
                 'NW': (-1, -1)}


def check_for_robot(row, column):
    return obstruction_space[row][column] == 'r'


def is_within_bounds(row, column):
    if 0 <= row < len(cleaning_space) and 0 <= column < len(cleaning_space[0]):
        return True
    else:
        return False


def check_for_wall(row, column):
    return obstruction_space[row][column] == 'w'


def check_for_cat(row, column):
    return obstruction_space[row][column] == 'c'


def move_cat(cat_current_row, cat_current_column, row_displacement, column_displacement, vacuum):
    cat_new_row = cat_current_row + row_displacement
    cat_new_column = cat_current_column + column_displacement

    if is_within_bounds(cat_new_row, cat_new_column) and obstruction_space[cat_new_row][cat_new_column] is None \
            and not check_for_wall(cat_new_row, cat_new_column) and not check_for_robot(cat_new_row, cat_new_column):
        obstruction_space[cat_new_row][cat_new_column] = 'c'
        obstruction_space[cat_current_row][cat_current_column] = None
        context['flag'] = False
        change_orientation(vacuum)

    else:
        context['flag'] = False
        change_orientation(vacuum)


def forward(vacuum: list):
    row, column, direction = vacuum

    row_displacement = displacements.get(direction)[0]
    column_displacement = displacements.get(direction)[1]

    new_row = row + row_displacement
    new_column = column + column_displacement

    if not is_within_bounds(new_row, new_column):
        context['flag'] = False
        change_orientation(vacuum)
        return

    if check_for_wall(row, column):
        context['flag'] = False
        change_orientation(vacuum)
        return

    if check_for_cat(new_row, new_column):
        move_cat(new_row, new_column, row_displacement, column_displacement, vacuum)
        return

    if check_for_robot(new_row, new_column):
        change_orientation(vacuum, "turn-left")
        return "turn-left"

    current_location = cleaning_space[row][column]
    next_location = cleaning_space[new_row][new_column]
    if current_location == 'd':
        match next_location:
            case None:
                cleaning_space[new_row][new_column] = 'd'
            case 'l':
                cleaning_space[new_row][new_column] = 'm'
            case 's':
                cleaning_space[new_row][new_column] = None

    elif current_location in ('l', 's'):
        skip_row, skip_column = new_row, new_column
        final_row, final_column = new_row + row_displacement, new_column + column_displacement

        if is_within_bounds(final_row, final_column) and not check_for_wall(final_row, final_column):
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

            skipped_position = cleaning_space[skip_row][skip_column]

            match skipped_position:
                case None:
                    cleaning_space[skip_row][skip_column] = 'l'
                case 'd':
                    cleaning_space[skip_row][skip_column] = 'm'
                case 's':
                    cleaning_space[skip_row][skip_column] = None

            cleaning_space[row][column] = None

            vacuum[0], vacuum[1] = final_row, final_column
            obstruction_space[final_row][final_column] = 'r'
            obstruction_space[row][column] = None
            return

        else:
            context['flag'] = False
            change_orientation(vacuum)
            return

    elif current_location == 'm':
        cleaning_space[new_row][new_column] = 'm'

    if check_for_wall(new_row, new_column):
        context['flag'] = False
        change_orientation(vacuum)
        return

    if check_for_cat(new_row, new_column):
        move_cat(new_row, new_column, row_displacement, column_displacement, vacuum)
        return

    if check_for_robot(new_row, new_column):
        change_orientation(vacuum, "turn-left")
        return "turn-left"

    vacuum[0], vacuum[1] = new_row, new_column
    obstruction_space[new_row][new_column] = 'r'
    obstruction_space[row][column] = None


def change_orientation(vacuum: list, command="turn-right"):
    index = directions.index(vacuum[2])
    if command == "turn-right":
        new_index = (index + 1) % len(directions)
        vacuum[2] = directions[new_index]
    if command == "turn-left":
        new_index = (index - 1) % len(directions)
        vacuum[2] = directions[new_index]


def clean(vacuum: list):
    if cleaning_space[vacuum[0]][vacuum[1]] == 'd':
        cleaning_space[vacuum[0]][vacuum[1]] = None


def vacuum_action(vacuum: list, action: str) -> str:
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
    if cleaning_space[vacuum[0]][vacuum[1]] == 'l':
        cleaning_space[vacuum[0]][vacuum[1]] = None


def perform_cleaning(instructions, vacuums, logs):
    with open(instructions, 'r') as input_file:
        lines = [line.strip() for line in input_file if line.strip()]

    for log_path in logs:
        with open(log_path, 'w'):
            continue


    for line in lines:
        robot_index, actions = line.split(maxsplit = 1)
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

