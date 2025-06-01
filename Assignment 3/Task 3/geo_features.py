from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Location:
    Y: int = 0
    X: int = 0

    def __str__(self):
        return f"({self.Y},{self.X})"


@dataclass
class Size:
    height: int = 0
    width: int = 0


class GeoFeature(ABC):
    def __init__(self, row, column, name, value):
        self.location = Location(row, column)
        self.name = name
        self.value = value

    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def return_symbol(self):
        pass


class Mountain(GeoFeature):

    def __init__(self, row, column, name, height):
        super().__init__(row, column, name, height)

    def get_size(self):
        return self.value

    def return_symbol(self):
        return 'm'


class Lake(GeoFeature):
    def __init__(self, row, column, name, depth):
        super().__init__(row, column, name, depth)

    def get_size(self):
        return self.value

    def return_symbol(self):
        return 'l'


class Crater(GeoFeature):
    def __init__(self, row, column, name, perimeter):
        super().__init__(row, column, name, perimeter)

    def get_size(self):
        return self.value

    def return_symbol(self):
        return 'c'
