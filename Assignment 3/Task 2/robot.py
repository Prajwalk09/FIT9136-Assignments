import geo_features
import math


class Robot:

    def __init__(self, size, features):
        self.start_location = geo_features.Location(0, 0)
        self.current_location = geo_features.Location(0, 0)
        self.journey = []
        self.start_day = 1
        self.size = size
        self.speeds = {
            'mountain': 6.0,
            'lake': 8.0,
            'crater': 10.0
        }
        self.features = {(f.location.Y, f.location.X): f for f in features}

    def moveto(self, target_row, target_column):
        if (target_row, target_column) == (self.current_location.Y, self.current_location.X):
            print("same location")
            return

        travel_path = [geo_features.Location(self.current_location.Y, self.current_location.X)]

        current_row, current_column = self.current_location.Y, self.current_location.X
        final_row, final_column = target_row, target_column

        horizontal_displacement = final_column - current_column
        vertical_displacement = final_row - current_row

        height, width = self.size.height, self.size.width

        direct_horizontal_path = abs(horizontal_displacement)
        wrapped_path = width - direct_horizontal_path

        if wrapped_path <= direct_horizontal_path:
            step = -1 if horizontal_displacement > 0 else 1
            moves = wrapped_path
        else:
            step = 1 if horizontal_displacement > 0 else -1
            moves = direct_horizontal_path
        for i in range(moves):
            current_column = (current_column + step) % width
            travel_path.append(geo_features.Location(current_row, current_column))

        direct_vertical_path = abs(vertical_displacement)
        wrapped_path = height - direct_vertical_path

        if wrapped_path <= direct_vertical_path:
            step_vertical = -1 if vertical_displacement > 0 else 1
            moves = wrapped_path
        else:
            step_vertical = 1 if vertical_displacement > 0 else -1
            moves = direct_vertical_path

        for i in range(moves):
            current_row = (current_row + step_vertical) % height
            travel_path.append(geo_features.Location(current_row, travel_path[-1].X))

        days = len(travel_path) - 1
        start, end = self.start_day, self.start_day + days - 1
        self.journey.append({'start': start, 'end': end,
                             'action': 'move', 'path': travel_path
                             })
        self.start_day = end + 1
        self.current_location = geo_features.Location(target_row, target_column)
        print(f"move from {travel_path[0]} to {travel_path[-1]}")

    def explore(self):
        key = (self.current_location.Y, self.current_location.X)
        feature = self.features.get(key)

        if not feature:
            print("nothing to explore")
            return
        else:
            feature_type = type(feature).__name__.lower()
            size = feature.get_size()
            speed = self.speeds.get(feature_type)
            days_required = math.ceil(size / speed)
            start, end = self.start_day, self.start_day + days_required - 1
            self.journey.append({'start': start, 'end': end,
                                 'action': 'explore', 'type': feature_type.lower(),
                                 'name': feature.name
                                 })
            self.start_day = end + 1
            self.speeds[feature_type] *= 1.2
            print(f"explore {feature_type.lower()} {feature.name}")

    def display_journey(self):
        if len(self.journey) == 0:
            print()
            return
        else:
            for item in self.journey:
                if item['start'] == item['end']:
                    label = f"Day {item['start']}:"
                else:
                    label = f"Day {item['start']}-{item['end']}:"

                if item['action'] == 'move':
                    value = " -> ".join(str(p) for p in item['path'])
                    print(f"{label} move {value}")
                else:
                    print(f"{label} explore {item['type']} {item['name']}")
