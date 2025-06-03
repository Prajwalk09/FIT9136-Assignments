import geo_features


def load_features() -> tuple:
    """
    This function is used to load all the features from the geo_features.txt file. This function reads the text file and
    performs the required computation.

    Parameters:
        This function does not take any parameters.
    Returns:
        This function returns size (geoFeatures.Size type) and all_features (dict type)
        The size variable contains the size of the grid which was given in the txt file.
        The all_features dictionary acts as a mapping between the location in the grid and the geological feature
        present at that location(if any). The keys are location and the values are the geological feature object
        present at that location.
    """
    all_features = {}
    with open('geo_features.txt') as input_file:
        # Opening and reading the file.
        file_data = input_file.readlines()
        map_size = file_data[0].strip().split(',')

        # Create a Size object using the size read from the file.
        size = geo_features.Size(int(map_size[0]), int(map_size[1]))

        # Reading each line after the first line.
        for line in file_data[1:]:
            feature_information = line.strip().split(',')
            # Extracting feature details
            feature_row, feature_column, feature_type, feature_name, feature_value = feature_information

            # Extracting location information and feature value (height, depth or perimeter)
            location = (int(feature_row), int(feature_column))
            feature_value = int(feature_value)

            # Depending on the feature type, instantiate an object of the corresponding class
            # with the right set of values.
            if feature_type == 'mountain':
                feature = geo_features.Mountain(location, feature_name, feature_value)
            elif feature_type == 'lake':
                feature = geo_features.Lake(location, feature_name, feature_value)
            elif feature_type == 'crater':
                feature = geo_features.Crater(location, feature_name, feature_value)
            all_features[location] = feature

    # Return size and all_features
    return size, all_features


def show_map(size:geo_features.Size, features:dict) -> None:
    """
    This function is used to display the map of the grid to the user. This function takes size and features as inputs.

    Parameters:
    size (geo_features.Size): This is a size object which gives information about the size of the grid.
    features (dict):  The features dictionary acts as a mapping between the location in the grid and the geological
                        feature present at that location(if any)

    Returns:
        This function does not return anything. It just displays the map to the user.
    """
    for height in range(size.height):
        row = []
        for width in range(size.width):
            location = (height, width)
            # If a feature is present at that location, display the feature's symbol, or else just display a .
            row.append(features[location].symbol() if location in features.keys() else '.')
        print(''.join(row))


def info_at(y:int, x:int, features:dict) -> None:
    """
    This function is used to print the details of a geological feature at a particular given location, if a feature
    exists at that location.

    Parameters:
        y(int): An integer value representing the row location in the grid
        x(int): An integer value representing the column location in the grid
        features (dict):  The features dictionary acts as a mapping between the location in the grid and the geological
                        feature present at that location(if any)
    Returns:
        This function does not return anything
    """
    # If the location is present in the features dictionary, call the describe method of the feature present at that
    # location or else print no information found.
    if (y, x) in features.keys():
        features[(y, x)].describe()
    else:
        print("no information found")


if __name__ == "__main__":
    # Load the size and feature variables
    size, features = load_features()
    while True:
        user_input = input('> ')

        # Case when the user inputs show_map
        if user_input == "show map":
            show_map(size, features)

        # Case when the user wants the information at a location
        elif user_input.split(' ')[0] == "info":
            # Extract the row and column values from the user input
            row, column = user_input.split(' ')[1:]
            info_at(int(row), int(column), features)

        # Case when the user inputs quit
        elif user_input == 'quit':
            print("goodbye")
            break

        # In case of any other input, continue to the next iteration
        else:
            continue
