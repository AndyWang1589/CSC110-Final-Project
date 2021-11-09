"""
data_functions by Andy Wang
=======================================================================================
This Python module contains functions that load and manipulate fire season data.

  - get_fire_data
  - predict_fire_season_data
  - extrapolate_num_fires
  - extrapolate_acreages
  - predict_next_top_five
  - predict_next_five_counties
  - predict_cause
=======================================================================================
Copyright (c) 2020 Andy Wang
"""
import random
from typing import Dict, List
from scrollable_classes import *


def get_fire_data(filename: str) -> Dict[int, CaliFireSeason]:
    """
    Parse through the given file and return a dictionary of california fire seasons.
    Each key is the year, and the value is that year's fire season.

    Preconditions:
      - filename != ""
    """
    data_so_far = {}

    # The way the file should be structured:
    # Year
    # Next five lines should be data about the top five fires of that year
    # After that should be data about the fire season itself
    # Repeats for the next year
    with open(filename) as fire_data:
        split_data = [row.split(',') for row in list(fire_data)]
        top_five_fires = []
        curr_year = None
        for entry in split_data:
            if len(entry) == 1:  # Introducing a year
                curr_year = int(entry[0])
            elif not entry[0].isnumeric():
                # If the first element is name of a county, it's a CaliFire datatype
                county = entry[0]
                acreage = int(entry[1])
                cause = entry[2]
                destroyed = int(entry[3])
                top_five_fires.append(CaliFire(curr_year, county, acreage, cause, destroyed))
            else:  # Otherwise, it's a fire season
                # By this time, the season's top five fires should have already been parsed
                num_fires = int(entry[0])
                acreage = int(entry[1])
                fire_season = CaliFireSeason(curr_year,
                                             num_fires,
                                             acreage,
                                             top_five_fires)
                data_so_far[curr_year] = fire_season
                top_five_fires = []  # Reset the top five

    return data_so_far


def predict_fire_season_data(seasons: Dict[int, CaliFireSeason], n: int) -> None:
    """
    Given a dictionary of fire seasons, predict the next n fire seasons by mutating the original
    dictionary by adding data for the next n fire seasons.

    Preconditions:
      - seasons != {}
      - n > 0
    """
    all_years = [seasons[year].year for year in seasons]
    all_num_fires = [seasons[year].fires for year in seasons]
    all_acreage = [seasons[year].acreage for year in seasons]
    all_counties = []

    counties_causes = {}  # A dict that maps a county to all the causes of its fires
    for year in seasons:
        for fire in seasons[year].top_five:
            all_counties.append(fire.county)
            if fire.county not in counties_causes:
                counties_causes[fire.county] = []
            counties_causes[fire.county].append(fire.cause)

    # Predict the number of fires and acreages for the next n seasons using extrapolation
    next_fires = extrapolate_num_fires(all_years, all_num_fires, n)
    next_acreages = extrapolate_acreages(all_num_fires, all_acreage, next_fires)

    for i in range(1, n + 1):
        year = 2020 + i
        fires = next_fires[i - 1]
        acreage = next_acreages[i - 1]
        top_five = predict_next_top_five(year, all_counties, counties_causes)
        seasons[year] = CaliFireSeason(year, fires, acreage, top_five)


def extrapolate_num_fires(years: List[int], fires: List[int], n: int) -> List[int]:
    """
    Given a list of total # of fires, extrapolate the next n # of fires using the line of best fit.

    Preconditions:
      - years != []
      - fires != []
      - n > 0
    """

    def f(x: int) -> int:
        """
        This is the function to extrapolate data.
        """
        return int(a + x * b)

    # Perform linear extrapolation
    # years are the x value, and fires are the y value
    avr_x = sum(years) / len(years)
    avr_y = sum(fires) / len(fires)

    b_numerator = sum(
        (years[i] - avr_x) * (fires[i] - avr_y)
        for i in range(len(fires))
    )
    b_denominator = sum(
        (years[i] - avr_x) ** 2
        for i in range(len(years))
    )

    b = b_numerator / b_denominator
    a = avr_y - b * avr_x

    fires_so_far = []
    for i in range(1, n + 1):
        year = 2020 + i
        fires_so_far.append(f(year))

    return fires_so_far


def extrapolate_acreages(fires: List[int], acreages: List[int], next_fires: List[int]) -> List[int]:
    """
    Extrapolate acreages based on the linear regression model of the
    relationship between num fires and acreage.

    One would expect that the more fires there are the higher the acreage.

    Preconditions:
      - fires != []
      - acreages != []
      - next_fires != []
    """

    def f(x: int) -> int:
        """
        This is the function to extrapolate data.
        """
        return int(a + x * b)

    # x is years, y is acreage
    avr_x = sum(fires) / len(fires)
    avr_y = sum(acreages) / len(acreages)

    b_numerator = sum(
        (fires[i] - avr_x) * (acreages[i] - avr_y)
        for i in range(len(fires))
    )
    b_denominator = sum(
        (fires[i] - avr_x) ** 2
        for i in range(len(fires))
    )

    b = b_numerator / b_denominator
    a = avr_y - b * avr_x

    acreages_so_far = []
    for fire in next_fires:
        acreages_so_far.append(f(fire))

    return acreages_so_far


def predict_next_top_five(year: int, counties: List[str],
                          counties_causes: Dict[str, List[str]]) -> List[CaliFire]:
    """
    Given a future year, # of fires, and acreage, determine the top five fires for that year.

    Preconditions:
      - counties != []
    """
    top_five_so_far = []
    five_counties = predict_next_five_counties(counties)

    for county in five_counties:
        causes = counties_causes[county]
        cause = predict_cause(causes)
        top_five_so_far.append(CaliFire(year, county, 90000, cause, 32))
        # Acreage and structures_destroyed are dummy variables,
        # since these can't be accurately predicted
        # these values won't be shown anyway

    return top_five_so_far


def predict_next_five_counties(counties: List[str]) -> List[str]:
    """
    Given a list of all the counties whose fires were in a season's top five,
    return five vulnerable counties.

    A county can appear multiple times in the list, meaning it is more likely
    to be chosen (ie. vulnerable)

    Preconditions:
      - counties != []
    """
    return [random.choice(counties) for _ in range(5)]


def predict_cause(causes: List[str]) -> str:
    """
    Given a list of all the causes of fires for a certain county, randomly pick one.

    A cause can appear multiple times, making it more likely to be chosen (ie. likely)

    Preconditions:
      - causes != []
    """
    return random.choice(causes)


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'W0401', 'E9999', 'E1101', 'E9998',
                    'E9969', 'E9988', '']
    })
