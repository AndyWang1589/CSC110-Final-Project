"""
main by Andy Wang
=======================================================================================
How has the increase in California's annual temperature affected the severity
(number of fires, acreage burned, structures destroyed) of California's
yearly wildfire seasons?

This Python module will open an interactive pygame window that displays the severity
of California's wildfires from 2008.
=======================================================================================
Copyright (c) 2020 Andy Wang
"""
import pygame
from data_functions import *
from graphics_functions import *
from scrollable_classes import *
from colour_fonts import *

# Constants
FUTURE_YEARS = 10  # Predict this many years into the future
SCROLL_SPEED = 15  # The num of pixels each scroll is
MAX_SCROLL = 600  # The limit of pixels you can scroll down for

if __name__ == "__main__":
    # Load all the data
    fire_season_data = get_fire_data("cali_fire_data.txt")
    predict_fire_season_data(fire_season_data, FUTURE_YEARS)
    years = list(fire_season_data.keys())

    # Main loop variable
    running = True

    # Misc variables for graphics
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    initial_map_coords = (190, 240)
    mapx, mapy = initial_map_coords
    scrollables = get_scrollables_for_season(fire_season_data[years[0]],
                                             Image(mapx, mapy, "county_map.jpg"))
    scroll_amount = 0
    curr_index = 0

    # Start the main pygame loop
    while running:
        # Get the user's mouse coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Get whatever key is pressed
        key = pygame.key.get_pressed()

        # Listen for keys
        if key[pygame.K_ESCAPE]:
            # Press ESC to quit
            running = False

        # Check for mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # You can also press the X button to quit, I'm not picky
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                scroll_direction = 1  # If this is 1, objects will move down
                if event.button == 5:
                    # Scroll down, so everything moves up,
                    # and thus the y coordinate is subtracted from
                    scroll_direction = -1
                scroll_translate = scroll_direction * SCROLL_SPEED

                if 0 <= scroll_amount - scroll_translate <= MAX_SCROLL:
                    scroll_objects(scrollables, scroll_translate)
                    scroll_amount -= scroll_translate

                    # If scroll_translate is positive,
                    # then you are scrolling back up (undoing your scroll)
                    # which means scroll_amount goes back to zero

                    # If scroll_translate is negative, then you are scrolling down
                    # so scroll_amount will increase

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    curr_index += 1
                    curr_index %= len(fire_season_data)
                elif event.key == pygame.K_LEFT:
                    curr_index -= 1
                    curr_index %= len(fire_season_data)
                scrollables = get_scrollables_for_season(fire_season_data[years[curr_index]],
                                                         Image(mapx, mapy, "county_map.jpg"))
                scroll_amount = 0  # reset the scroll amount

        specific_fire = get_mouse_on_fire_circle(mouse_x, mouse_y, scrollables)

        # Draw everything
        screen.fill(WHITE)
        draw_scrollables(screen, scrollables)

        if specific_fire is not None:
            display_county_fire_info(screen, specific_fire)
        display_season_data(screen, fire_season_data, curr_index)

        pygame.display.flip()
    pygame.display.quit()
