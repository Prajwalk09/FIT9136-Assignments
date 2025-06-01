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

    def __init__(self, location, name):
        """
        This is a constructor of the GeoFeature class
        :param location:
        :param name:
        """
        self.location = location
        self.name = name

    @abstractmethod
    def describe(self):
        pass

    @abstractmethod
    def symbol(self):
        pass


class Mountain(GeoFeature):

    def __init__(self, location, name, height):
        super().__init__(location, name)
        self.height = height

    def describe(self):
        print(f"{self.__class__.__name__.lower()} {self.name}, height {self.height}")

    def symbol(self):
        return "m"


class Lake(GeoFeature):

    def __init__(self, location, name, depth):
        super().__init__(location, name)
        self.depth = depth

    def describe(self):
        print(f"{self.__class__.__name__.lower()} {self.name}, depth {self.depth}")

    def symbol(self):
        return "l"


class Crater(GeoFeature):

    def __init__(self, location, name, perimeter):
        super().__init__(location, name)
        self.perimeter = perimeter

    def describe(self):
        print(f"{self.__class__.__name__.lower()} {self.name}, perimeter {self.perimeter}")

    def symbol(self):
        return "c"
