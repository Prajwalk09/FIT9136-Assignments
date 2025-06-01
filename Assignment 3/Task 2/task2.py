import geo_features
import robot


def load_features():
    all_features = []

    with open('geo_features.txt') as input_file:
        lines = [line.strip() for line in input_file if line.strip()]

        map_height, map_width = lines[0].split(',')[0], lines[0].split(',')[1]
        map_height, map_width = int(map_height), int(map_width)

        size = geo_features.Size(map_height, map_width)

        for line in lines[1:]:
            row, column, feature_type, name, value = [item.strip(',') for item in line.split(',')]
            row, column = int(row), int(column)
            value = float(value)

            if feature_type.lower() == 'mountain':
                all_features.append(geo_features.Mountain(row, column, name, value))
            elif feature_type.lower() == 'lake':
                all_features.append(geo_features.Lake(row, column, name, value))
            else:
                all_features.append(geo_features.Crater(row, column, name, value))

        return size, all_features


if __name__ == "__main__":
    size, all_features = load_features()
    robot = robot.Robot(size, all_features)

    while True:
        user_input = input("> ").strip().lower()

        if user_input == 'quit':
            print("goodbye")
            break
        elif user_input == "show map":
            for i in range(size.height):
                current_row = ""
                for j in range(size.width):
                    location = (i, j)
                    current_row += (type(robot.features[location]).__name__[0].lower()
                                    if location in robot.features else '.')
                print(current_row)
        elif user_input.startswith('moveto'):
            target_row, target_column = user_input.split(' ')[1], user_input.split(' ')[2]
            robot.moveto(int(target_row), int(target_column))
        elif user_input == 'explore':
            robot.explore()
        elif user_input == 'display journey':
            robot.display_journey()
        else:
            continue

    pass
