#!/usr/bin/env python3

# This is just a mock-up of the actual script

from datetime import datetime
import math
import time

SPOKES = 3
RADIUS_IN_INCHES = 1

CIRCUMFERENCE_IN_INCHES = 2 * math.pi * RADIUS_IN_INCHES
START_DATETIME = datetime.now()
ROUND_TO_VALUE = 5

number_of_breaks = 0
revolutions = 0


def laser_break_callback(beam_is_broken):
    if beam_is_broken:
        global number_of_breaks
        global revolutions

        if number_of_breaks % SPOKES == 0:
            distance_traveled_in_miles_rounded = calculate_distance_traveled_in_miles(revolutions, CIRCUMFERENCE_IN_INCHES, ROUND_TO_VALUE)
            revolutions_per_minute_rounded = calculate_revolutions_per_minute(revolutions, START_DATETIME, ROUND_TO_VALUE)

            print(f"Revolutions: {revolutions} | Miles: {distance_traveled_in_miles_rounded} | RPM: {revolutions_per_minute_rounded}")

            revolutions += 1

        number_of_breaks += 1


def calculate_distance_traveled_in_miles(revolutions, circumference_in_inches, round_to_value):
    distance_traveled_in_inches = revolutions * circumference_in_inches
    distance_traveled_in_feet = distance_traveled_in_inches / 12
    distance_traveled_in_miles = distance_traveled_in_feet / 5280

    return round(distance_traveled_in_miles, round_to_value)


def calculate_revolutions_per_minute(revolutions, start_datetime, round_to_value):
    time_elapsed_in_seconds = (datetime.now() - start_datetime).total_seconds()
    time_elapsed_in_minutes = time_elapsed_in_seconds / 60

    revolutions_per_minute = revolutions / time_elapsed_in_minutes

    return round(revolutions_per_minute, round_to_value)


def main():
    while True:
        sleep_time_in_seconds = 0.025
        laser_break_callback(True)
        time.sleep(sleep_time_in_seconds)
        laser_break_callback(False)
        time.sleep(sleep_time_in_seconds)


if __name__ == "__main__":
    main()
