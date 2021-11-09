"""
fire_classes by Andy Wang
=======================================================================================
This Python module contains the dataclass definitions for CaliFireSeason and CaliFire.
=======================================================================================
Copyright (c) 2020 Andy Wang
"""
from dataclasses import dataclass
from typing import List


@dataclass
class CaliFire:
    """
    A dataclass representing a single fire in California.

    Instance Attributes:
      - year: the year in which the fire took place (>0 for AD, <0 for BC)
      - county: the Californian county in which the fire took place
      - acreage: how many acres of land were burned in this fire
      - cause: the reported cause of the fire
      (Note: I'm treating Under Investigation as the same as Unknown)
      - structures_destroyed: how many structures were destroyed in the fire

    Representation Invariants:
      - self.county != ""
      - self.acreage > 0
      - self.cause != ""
      - self.structures_destroyed > -1

    >>> butte = CaliFire(2008, "Butte", 47647, "Lightning", 117)
    >>> butte.county == "Butte"
    True
    >>> butte.cause == "Lightning"
    True
    """
    year: int
    county: str
    acreage: int
    cause: str
    structures_destroyed: int


@dataclass
class CaliFireSeason:
    """
    A dataclass representing a California fire season.

    Instance Attributes:
      - year: the year of the season (>0 for AD, <0 for BC)
      - fires: how many major fires occured in California in that year
      - acreage: how many acres of land were burned that year
      - top_five: the top five fires of the year, in order from most acreage to least

    Representation Invariants:
      - self.year != 0
      - self.fire > 0
      - self.acreage > 0
      - len(self.top_five) == 5

    >>> butte1 = CaliFire(2008, "Butte", 47647, "Lightning", 117)
    >>> mariposa = CaliFire(2008, "Mariposa", 34091, "Other", 133)
    >>> riverside = CaliFire(2008, "Riverside", 30305, "Structure", 245)
    >>> shasta = CaliFire(2008, "Shasta", 27936, "Lightning", 12)
    >>> butte2 = CaliFire(2008, "Butte", 23344, "Arson", 351)
    >>> top_five = [butte1, mariposa, riverside, shasta, butte2]
    >>> fire = CaliFireSeason(2008, 6255, 1593690, top_five)
    >>> fire.year == 2008
    True
    >>> fire.top_five[2] == riverside
    True
    >>> fire.acreage == 1593690
    True
    """
    year: int
    fires: int
    acreage: int
    top_five: List[CaliFire]


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'W0401', 'E9999', 'E1101', 'R0913']
    })

    import doctest

    doctest.testmod()
