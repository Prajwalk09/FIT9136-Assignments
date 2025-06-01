import geo_features
from robot import Robot


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
    robot = Robot(size, all_features)
    name_feature_mapping = {feature.name: feature for feature in all_features}

    transformation_speeds = {
        'Robot': {'mountain': 6.0, 'lake': 8.0, 'crater': 10.0},
        'Drone': {'mountain': 12.0, 'lake': 6.0, 'crater': 8.0},
        'AUV': {'mountain': 2.0, 'lake': 12.0, 'crater': 6.0}
    }

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

        elif user_input.startswith('mission'):
            mission, remaining_text = user_input.split(' ', maxsplit=1)
            feature_names = [item.strip() for item in remaining_text.split(',')]

            durations = {}

            for form in ['Robot', 'Drone', 'AUV']:
                durations[form] = robot.mission_function(form, feature_names)

            preferences = {'Robot': 0, 'Drone': 1, 'AUV': 2}
            best_form = min(durations, key=lambda item: (durations[item], preferences[item]))

            match best_form:
                case 'Robot':
                    print("no transformation")
                case 'Drone':
                    print("transform into a drone")
                case 'AUV':
                    print("transform into an AUV")

            new_robot = Robot(size, all_features)
            new_robot.speeds = transformation_speeds[best_form].copy()

            current_location_y, current_location_x = 0, 0

            for feature_name in feature_names:
                feature = name_feature_mapping[feature_name]
                feature_location_y, feature_location_x = feature.location.Y, feature.location.X

                path = [(current_location_y, current_location_x)]
                height, width = size.height, size.width

                horizontal_displacement = feature_location_x - current_location_x
                vertical_displacement = feature_location_y - current_location_y

                absolute_horizontal_displacement = abs(horizontal_displacement)
                absolute_vertical_displacement = abs(vertical_displacement)

                wrapped_horizontal = width - horizontal_displacement
                if wrapped_horizontal <= horizontal_displacement:
                    horizontal_step = -1 if horizontal_displacement > 0 else 1
                    steps_horizontal = wrapped_horizontal
                else:
                    horizontal_step = 1 if horizontal_displacement > 0 else -1
                    steps_horizontal = absolute_horizontal_displacement

                y, x = current_location_y, current_location_x
                for i in range(steps_horizontal):
                    x = (x + steps_horizontal) % width
                    path.append((y, x))

                wrapped_vertical = height - vertical_displacement

                if wrapped_vertical <= vertical_displacement:
                    vertical_step = -1 if vertical_displacement > 0 else 1
                    step_vertical = wrapped_vertical
                else:
                    vertical_step = 1 if vertical_displacement > 0 else -1
                    step_vertical = absolute_vertical_displacement

                for i in range(step_vertical):
                    y = (y + step_vertical) % height
                    path.append((x, y))

                print(f"move from ({current_location_y},{current_location_x}) to ({feature_location_y},{feature_location_x}) then explore {type(feature).__name__.lower()} {feature_name}")

                new_robot.moveto(feature_location_y, feature_location_x)
                new_robot.explore()

                current_location_y = feature_location_y
                current_location_x = feature_location_x
            continue
        else:
            continue

    pass
