import geo_features


def load_features():
    all_features = {}
    with open('geo_features.txt') as input_file:
        file_data = input_file.readlines()
        map_size = file_data[0].strip().split(',')
        size = geo_features.Size(int(map_size[0]), int(map_size[1]))

        for line in file_data[1:]:
            feature_information = line.strip().split(',')
            feature_row, feature_column, feature_type, feature_name, feature_value = feature_information

            location = (int(feature_row), int(feature_column))
            feature_value = int(feature_value)

            if feature_type == 'mountain':
                feature = geo_features.Mountain(location, feature_name, feature_value)
            elif feature_type == 'lake':
                feature = geo_features.Lake(location, feature_name, feature_value)
            elif feature_type == 'crater':
                feature = geo_features.Crater(location, feature_name, feature_value)
            all_features[location] = feature

    return size, all_features


def show_map(size, features):
    for height in range(size.height):
        row = []
        for width in range(size.width):
            location = (height, width)
            row.append(features[location].symbol() if location in features.keys() else '.')
        print(''.join(row))


def info_at(y, x, features):
    if (y, x) in features.keys():
        features[(y, x)].describe()
    else:
        print("no information Found")


if __name__ == "__main__":
    size, features = load_features()

    while True:
        user_input = input('> ')

        if user_input == "show map":
            show_map(size, features)
        elif user_input.split(' ')[0] == "info":
            row, column = user_input.split(' ')[1:]
            info_at(int(row), int(column), features)
        elif user_input == 'quit':
            print("goodbye")
            break
        else:
            continue
