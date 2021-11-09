"""
scrollable_classes by Andy Wang
========================================================================================
This Python module contains the class definition for the abstract ScrollableObject class,
and its concrete subclasses:
  - Image
  - TextLabel
  - FireCircle
========================================================================================
Copyright (c) 2020 Andy Wang
"""

from typing import Tuple
from fire_classes import *
from colour_fonts import *


class ScrollableObject:
    """
    An abstract class representing an object that can be scrolled on a pygame surface.
    """

    # Private Instance Attributes:
    #   - _x: the x coordinate of the object
    #   - _y: the y coordinate of the object
    # Note: The coordinates are either top-left or the centre, depending on the object
    _x: int
    _y: int

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the object at the specified coordinates.
        """
        self._x = x
        self._y = y

    def get_coords(self) -> Tuple[int, int]:
        """
        Return the coordinates of this object.
        """
        return (self._x, self._y)

    def translate(self, dx: int, dy: int) -> None:
        """
        Translate the object's coordinates.
        """
        self._x += dx
        self._y += dy

    def move_to(self, x: int, y: int) -> None:
        """
        Move the coordinates to the given ones.
        """
        self._x, self._y = x, y

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the object on the screen.
        """
        raise NotImplementedError


class Image(ScrollableObject):
    """
    A class representing an image to be drawn and scrolled on a pygame window.

    >>> image = Image(500, 500, "county_map.jpg")
    >>> image.get_coords()
    (500, 500)
    """
    # Private Instance Attributes:
    #   - _image: the image to draw
    _image: pygame.Surface

    def __init__(self, x: int, y: int, filename: str) -> None:
        """
        Initialize the image at the specified coordinates.

        Preconditions:
          - filename != ""
        """
        super().__init__(x, y)
        self._image = pygame.image.load(filename)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the image on the screen.
        """
        screen.blit(self._image, (self._x, self._y))

    def get_width(self) -> int:
        """
        Return the width in pixels of this image.
        """
        return self._image.get_width()

    def get_height(self) -> int:
        """
        Return the height in pixels of this image.
        """
        return self._image.get_height()


class FireCircle(ScrollableObject):
    """
    A class representing a single county fire visually with a circle.

    >>> from fire_classes import CaliFire
    >>> fire = CaliFire(2000, "County", 999, "You", 0)
    >>> circle = FireCircle(0, 0, [fire])
    >>> circle.get_fires()[0] == fire
    True
    """
    # Private Instance Attributes:
    #   - _year: the year of the fires
    #   - _county: the county that the fire takes place in, as a string
    #   - _acreage: the acreage of the fire
    #   - _fires: a list of all the fires that happened in this county, within the season's top five
    #             in order from most to least acreage
    #   - _radius: the radius of the circle
    #   - _colour: the colour of the circle

    # Representation Invariants:
    #   - self._county != ""
    #   - self._acreage > 0
    #   - self._fires != []
    #   - self._radius > 0
    #   - all(0 <= n <= 255 for n in self._colour)

    _county: str
    _acreage: int
    _fires: List[CaliFire]
    _radius: int
    _colour: Tuple[int, int, int]

    def __init__(self, x: int, y: int, fires: List[CaliFire]) -> None:
        """
        Create a FireCircle that represents all the fires that happened at a county,
        but only in the season's top five fires.

        Preconditions:
          - fires != []
        """
        super().__init__(x, y)
        self._county = fires[0].county  # they should all have the same county
        self._acreage = 0
        self._fires = fires

        if fires[0].year > 2020:
            self._colour = LIGHT_RED
            self._radius = 25
            # When the fire circle represents a predicted fire, don't bother with acreage
            # because there is too little data for each individual county to accurately predict it
            # when it is in the top five
        else:
            # Accumulate total acreage in the county - only for drawing purposes
            for fire in fires:
                self._acreage += fire.acreage

            # Dictionary of acreage bounds to colour and radius of circle
            bounds = {
                0: (YELLOW, 10),
                10000: (YELLOW, 12),
                20000: (YELLOW, 15),
                40000: (ORANGE, 18),
                60000: (ORANGE, 20),
                80000: (RED, 22),
                100000: (RED, 25),
            }

            for bound in bounds:
                if self._acreage >= bound:
                    self._colour, self._radius = bounds[bound]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the circle that represents this fire.
        """

        font = CALIBRI_14_B

        pygame.draw.circle(screen, self._colour, self.get_coords(), self._radius)

        width, height = font.size(self._county)
        text = font.render(self._county, True, BLACK)
        screen.blit(text, (self._x - width / 2, self._y - height / 2))

    def get_bounds(self) -> Tuple[int, int, int, int]:
        """
        Return coordinates and dimensions of the square that this circle takes up.
        """
        # Top-let coordinates
        x = self._x - self._radius
        y = self._y - self._radius

        return (x, y, self._radius * 2, self._radius * 2)

    def get_fires(self) -> List[CaliFire]:
        """
        Return all the county fires that this class is associated with.
        """
        return self._fires


class TextLabel(ScrollableObject):
    """
    A class representing very large, scrollable text.

    Instance Attributes:
      - text: the text to display

    Representation Invariants:
      - self.text != ""

    >>> from colour_fonts import CALIBRI_14_B
    >>> my_text = TextLabel(0, 0, "David sure is a glamorous individual", CALIBRI_14_B, (0, 0, 0))
    >>> my_text.text == "David sure is a glamorous individual"
    True
    """
    # Private Instance Attributes:
    #   - _font: the font to render the text with
    #   - _colour: the colour to render the text with

    # Representation Invariants:
    #   - all(0 <= n <= 255 for n in self._colour)

    text: str
    _font: pygame.font.Font
    _colour: Tuple[int, int, int]

    def __init__(self, x: int, y: int, text: str,
                 font: pygame.font.Font, colour: Tuple[int, int, int]) -> None:
        """
        Make a text box with top-left corner at (x, y), displaying text with specified font.

        Preconditions:
          - text != ""
          - all(0 <= num <= 255 for num in colour)
        """
        super().__init__(x, y)
        self.text = text
        self._font = font
        self._colour = colour

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the text box on the screen.
        """
        text = self._font.render(self.text, True, self._colour)
        screen.blit(text, self.get_coords())

    def centerize_width(self, screen_w: int) -> None:
        """
        Centres the text width-wise given the width of the screen.

        Preconditions:
          - screen_w > 0
        """
        text_w = self._font.size(self.text)[0]
        self._x = int(screen_w / 2 - text_w / 2)


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'W0401', 'E9999', 'E1101', 'R0913']
    })

    import doctest

    doctest.testmod()
