"""
graphics_functions by Andy Wang
=======================================================================================
This Python module contains functions that display things on a pygame screen.

  - draw_scrollables
  - get_scrollables_for_season
  - display_season_data
  - get_counties_on_map
  - display_county_fire_info
  - scroll_objects
  - get_mouse_on_fire_circle
  - draw_rect_outline
=======================================================================================
Copyright (c) 2020 Andy Wang
"""
from typing import Optional, Dict
from county_mapping import MAPPING
from scrollable_classes import *

# Constants for the screen
WIDTH = 800
HEIGHT = 800


def draw_scrollables(screen: pygame.Surface, scrollables: List[ScrollableObject]) -> None:
    """
    Draw all the provided drawable objects on the given screen.

    Preconditions:
      - scrollables != []
    """
    for scrollable in scrollables:
        scrollable.draw(screen)


def get_scrollables_for_season(season: CaliFireSeason,
                               img_map: Image) -> List[ScrollableObject]:
    """
    Given a season, return all the scrollables needed to
    display the data for it.
    """
    season_text = f"Total # of fires: {season.fires}    " \
                  f"Total acreage burned: {season.acreage}"
    map_text = "Top Five Fires:"

    if season.year > 2020:
        season_text = f"Total # of fires: ~{season.fires}    " \
                      f"Total acreage burned: ~{season.acreage}"
        map_text = "Five Vulnerable Counties:"
    season_data_label = TextLabel(0, 160,
                                  season_text,
                                  CALIBRI_24_B, BLACK)
    season_data_label.centerize_width(WIDTH)

    map_label = TextLabel(0, 200, map_text, CALIBRI_24_B, BLACK)
    map_label.centerize_width(WIDTH)

    scrollables_so_far = [season_data_label, map_label, img_map]
    county_circles = get_counties_on_map(season, img_map)
    scrollables_so_far += county_circles
    return scrollables_so_far


def display_season_data(screen: pygame.Surface, seasons: Dict[int, CaliFireSeason],
                        current_index: int) -> None:
    """
    Display the # of fires and acreage data for the fire seasons
    on the top of the screen.

    The season at current_index is highlighted, since it is the
    season that the user is focusing on.

    Preconditions:
      - seasons != {}
      - 0 <= current_index < len(seasons)
    """
    seasons_list = [seasons[s] for s in seasons]
    years = list(seasons.keys())

    horiz_edge_offset = 20  # Distance from edge of the screen horizontally
    vert_edge_offset = 10  # Distance from top of the screen
    section_height = 100  # the height of a section in pixels

    # The total horizontal width of the entire graph
    total_width = WIDTH - (2 * horiz_edge_offset)

    section_width = total_width / len(seasons)
    section_offset = 5  # gap between bar and the edge of the section
    bar_width = (section_width - 2 * section_offset) / 2  # two bars in each section

    all_num_fires = [season.fires for season in seasons_list]
    all_acreage = [season.acreage for season in seasons_list]
    max_num_fires = max(all_num_fires)
    max_acreage = max(all_acreage)

    # Draw the background for the graph
    background = pygame.Rect(0, 0, total_width, section_height + 3 * vert_edge_offset)
    pygame.draw.rect(screen, WHITE, background)

    # Initialize fonts
    font = CALIBRI_14_B
    num_fires_text = font.render("# of Fires", True, RED)
    num_fires_text = pygame.transform.rotate(num_fires_text, 90)
    screen.blit(num_fires_text, (horiz_edge_offset / 4,
                                 section_height / 2 - vert_edge_offset))

    acreage_text = font.render("Acreage", True, ORANGE)
    acreage_text = pygame.transform.rotate(acreage_text, 90)
    screen.blit(acreage_text, (WIDTH - horiz_edge_offset,
                               section_height / 2 - vert_edge_offset))

    for x in range(len(seasons)):
        # x-coordinate of the section
        section_x = horiz_edge_offset + x * section_width

        # red bar is # of fires, orange is acreage
        red_bar_x = section_x + section_offset
        orange_bar_x = red_bar_x + bar_width

        red_bar_height = int((all_num_fires[x] / max_num_fires)
                             * (section_height - vert_edge_offset))
        orange_bar_height = int((all_acreage[x] / max_acreage)
                                * (section_height - vert_edge_offset))

        # Make all the bars stand on the same level
        red_bar_y = section_height - red_bar_height + vert_edge_offset
        orange_bar_y = section_height - orange_bar_height + vert_edge_offset

        # Draw the stuff
        if x == current_index:
            highlight = pygame.Rect(section_x, 0, section_width,
                                    section_height + 3 * vert_edge_offset)
            pygame.draw.rect(screen, LIGHT_BLUE, highlight)

        red_bar = pygame.Rect(red_bar_x, red_bar_y, bar_width, red_bar_height)
        orange_bar = pygame.Rect(orange_bar_x, orange_bar_y, bar_width, orange_bar_height)

        if years[x] > 2020:
            pygame.draw.rect(screen, LIGHT_RED, red_bar)
            pygame.draw.rect(screen, LIGHT_ORANGE, orange_bar)
        else:
            pygame.draw.rect(screen, RED, red_bar)
            pygame.draw.rect(screen, ORANGE, orange_bar)

        # Draw the bar's text
        year_text = font.render(str(years[x]), True, BLACK)
        text_width = font.size(str(years[x]))[0]
        screen.blit(year_text, ((section_x + section_width / 2) - text_width / 2,
                                red_bar_y + red_bar_height + section_offset / 2))

        # A bar with a border in it means it's the highest
        if all_num_fires[x] == max_num_fires:
            draw_rect_outline(screen, red_bar, BLACK, 3)

        if all_acreage[x] == max_acreage:
            draw_rect_outline(screen, orange_bar, BLACK, 3)


def get_counties_on_map(season: CaliFireSeason, img_map: Image) -> List[FireCircle]:
    """
    Add circles to the list of scrollables, that each represent a single county fire.

    The larger and redder the circle, the more acreage was burned.
    """
    circles_so_far = []
    # The fact that a county can have multiple fires makes this a bit more complicated
    # Make a dictionary that maps a county name to a list of fires there
    fire_dict = {}
    for fire in season.top_five:
        if fire.county not in fire_dict:
            fire_dict[fire.county] = []
        fire_dict[fire.county].append(fire)

    for county in fire_dict:
        x1, y1 = MAPPING[county]
        x2, y2 = img_map.get_coords()

        fires = fire_dict[county]
        circles_so_far.append(FireCircle(x1 + x2, y1 + y2, fires))

    return circles_so_far


def display_county_fire_info(screen: pygame.Surface, circle: FireCircle) -> None:
    """
    When the mouse is hovering over a fire circle, display data about
    all the fires that happened in that county, within the current season's top five.
    """
    fires = circle.get_fires()
    year = fires[0].year
    width = 200
    height_per_fire = 90  # Each fire that happens at a county is given this many pixels vertically
    # to display its info

    if year > 2020:
        height_per_fire = 45

    x, y = circle.get_coords()
    edge_offset = width / 25
    text_gap = 20

    display_rect = pygame.Rect(x, y, width, height_per_fire * len(fires))

    pygame.draw.rect(screen, WHITE, display_rect)

    font = CALIBRI_14_B
    for i, fire in enumerate(fires):
        height = y + i * height_per_fire
        if i >= 1:
            pygame.draw.line(screen, BLACK,
                             (x, height), (x + width, height), 1)
        county = fire.county
        acreage = str(fire.acreage)
        cause = fire.cause
        destroyed = fire.structures_destroyed

        first_line_y = height + edge_offset

        if year > 2020:
            screen.blit(font.render(f"County: {county}", True, BLACK),
                        (x + edge_offset, first_line_y))
            screen.blit(font.render(f"Most Likely Cause: {cause}", True, BLACK),
                        (x + edge_offset, first_line_y + text_gap))
        else:
            screen.blit(font.render(f"County: {county}", True, BLACK),
                        (x + edge_offset, first_line_y))
            screen.blit(font.render(f"Acreage: {acreage}", True, BLACK),
                        (x + edge_offset, first_line_y + text_gap))
            screen.blit(font.render(f"Cause: {cause}", True, BLACK),
                        (x + edge_offset, first_line_y + 2 * text_gap))
            screen.blit(font.render(f"Structures destroyed: {destroyed}", True, BLACK),
                        (x + edge_offset, first_line_y + 3 * text_gap))

    draw_rect_outline(screen, display_rect, BLACK, 1)


def scroll_objects(scrollables: List[ScrollableObject], scroll_amount: int) -> None:
    """
    Scroll all the provided drawable objects on the given screen by scroll_amount pixels.

    If scroll > 0, move everything down. If scroll < 0, move everything up.

    Preconditions:
      - scrollables != []
      - scroll_amount > 0
    """
    for scrollable in scrollables:
        scrollable.translate(0, scroll_amount)


def get_mouse_on_fire_circle(x: int, y: int,
                             scrollables: List[ScrollableObject]) -> Optional[FireCircle]:
    """
    Return whether the coords (x, y) are in a fire circle, and
    return that circle if yes.

    Preconditions:
      - scrollables != []
    """
    for scrollable in scrollables:
        if isinstance(scrollable, FireCircle):
            cx, cy, w, h = scrollable.get_bounds()

            if (cx < x < cx + w) and (cy < y < cy + h):
                return scrollable

    return None


def draw_rect_outline(screen: pygame.Surface, rect: pygame.Rect,
                      colour: Tuple[int, int, int], thickness: int) -> None:
    """
    Draw an outline around the given rectangle, given that the rectangle
    is drawn before this functio is called.
    """
    x = rect.x
    y = rect.y
    w = rect.width
    h = rect.height

    # Top border
    pygame.draw.line(screen, colour, (x, y), (x + w, y), thickness)
    # Bottom line
    pygame.draw.line(screen, colour, (x, y + h), (x + w, y + h), thickness)
    # Left border
    pygame.draw.line(screen, colour, (x, y), (x, y + h), thickness)
    # Right border
    pygame.draw.line(screen, colour, (x + w, y), (x + w, y + h), thickness)


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'W0401', 'E9999', 'E1101', 'E9998',
                    'E9969', 'E9988', 'R0914']
    })
