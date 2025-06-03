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

    def __init__(self, location, name:str) -> None:
        """
        This is a constructor of the GeoFeature class. Since the GeoFeature is an abstract base class, objects of this
        class cannot be created, but this constructor can be called in the child class's constructor to set appropriate
        values.

        Parameters:
            location(tuple): A tuple of integers containing the location of the Geological feature in the grid.
            name(str): A string value representing the name of the feature.

        Returns:
            This function does not return anything. It is only used to initialise objects everytime they are created.
        """
        self.location = location
        self.name = name

    # Defining 2 abstract methods which WILL be implemented by child classes
    @abstractmethod
    def describe(self):
        pass

    @abstractmethod
    def symbol(self):
        pass


class Mountain(GeoFeature):

    def __init__(self, location, name:str, height:int) -> None:
        """
        This is a constructor of the Mountain class. This constructor is called everytime an object of the Mountain class
        is created. This constructor also makes a call to the parent class constructor.

        Parameters:
            location(tuple): A tuple of integers containing the location of the Geological feature in the grid.
            name(str): A string value representing the name of the feature.
            height(int): An integer value representing the height of the mountain

        Returns:
            This function does not return anything.
        """
        # Making a call to the parent class constructor
        super().__init__(location, name)
        self.height = height

    def describe(self):
        """
        This function is used to describe features each object of the Mountain class holds. It prints the class name,
        name of the feature and its height.

        Parameters:
            This function takes no parameters
        Returns:
            This function does not return anything. It just outputs a print statement.
        """
        print(f"{self.__class__.__name__.lower()} {self.name}, height {self.height}")

    def symbol(self) -> str:
        """
        This is a helper function which is used to return a symbol. This function takes no inputs.

        Returns:
            This function returns 'm'. Which in this case signifies Mountain
        """
        return "m"


class Lake(GeoFeature):

    def __init__(self, location, name:str, depth:int) -> None:
        """
        This is a constructor of the Lake class. This constructor is called everytime an object of the Lake class
        is created. This constructor also makes a call to the parent class constructor.

        Parameters:
            location(tuple): A tuple of integers containing the location of the Geological feature in the grid.
            name(str): A string value representing the name of the feature.
            depth(int): An integer value representing the depth of the lake.

        Returns:
            This function does not return anything.
                """
        # Making a call to the parent class constructor
        super().__init__(location, name)
        self.depth = depth

    def describe(self) -> None:
        """
        This function is used to describe features each object of the Lake class holds. It prints the class name,
        name of the feature and its depth.

        Parameters:
            This function takes no parameters
        Returns:
            This function does not return anything. It just outputs a print statement.
        """
        print(f"{self.__class__.__name__.lower()} {self.name}, depth {self.depth}")

    def symbol(self) -> str:
        """
        This is a helper function which is used to return a symbol. This function takes no inputs.

        Returns:
            This function returns 'l'. Which in this case signifies Lake
        """
        return "l"


class Crater(GeoFeature):

    def __init__(self, location, name:str, perimeter:int) -> None:
        """
        This is a constructor of the Lake class. This constructor is called everytime an object of the Lake class
        is created. This constructor also makes a call to the parent class constructor.

        Parameters:
            location(tuple): A tuple of integers containing the location of the Geological feature in the grid.
            name(str): A string value representing the name of the feature.
            perimeter(int): An integer value representing the perimeter of the crater.

        Returns:
            This function does not return anything.
        """
        # Making a call to the parent class constructor
        super().__init__(location, name)
        self.perimeter = perimeter

    def describe(self):
        """
        This function is used to describe features each object of the Crater class holds. It prints the class name,
        name of the feature and its perimeter.

        Parameters:
            This function takes no parameters
        Returns:
            This function does not return anything. It just outputs a print statement.
        """
        print(f"{self.__class__.__name__.lower()} {self.name}, perimeter {self.perimeter}")

    def symbol(self) -> str:
        """
        This is a helper function which is used to return a symbol. This function takes no inputs.

        Returns:
            This function returns 'c'. Which in this case signifies Crater
        """
        return "c"
