#!/usr/bin/env python3

import csv
import os

import RPi.GPIO as GPIO

from datetime import datetime
from gpiozero import CPUTemperature
from pathlib import Path
from sense_hat import SenseHat
from fanshim import FanShim

def convert_celsius_to_fehrenheit(celsius):
    return ((celsius / 5) * 9) + 32


def get_data_row_dictionary():
    decimal_places = 1

    # TODO: Refactor
    cpu_temperature_celsius = CPUTemperature().temperature
    cpu_temperature_fehrenheit = convert_celsius_to_fehrenheit(cpu_temperature_celsius)
    cpu_temperature_celsius_rounded = round(cpu_temperature_celsius, decimal_places)
    cpu_temperature_fehrenheit_rounded = round(cpu_temperature_fehrenheit, decimal_places)

    sense_hat_temperature_celsuis = SenseHat().get_temperature()
    sense_hat_temperature_fehrenheit = convert_celsius_to_fehrenheit(sense_hat_temperature_celsuis)
    sense_hat_temperature_celsuis_rounded = round(sense_hat_temperature_celsuis, decimal_places)
    sense_hat_temperature_fehrenheit_rounded = round(sense_hat_temperature_fehrenheit, decimal_places)

    # fan_shim_pin = 18
    # GPIO.setwarnings(False)
    # state = GPIO.input(fan_shim_pin)

    state = None

    if state:
        fan_sime_sate = "Running"
    else:
        fan_sime_sate = "Off"

    data_row_dictionary = {
        "Timestamp": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p"),
        "CPU Temperature C": cpu_temperature_celsius_rounded,
        "CPU Temperature F": cpu_temperature_fehrenheit_rounded,
        "Sense Hat Temperature C": sense_hat_temperature_celsuis_rounded,
        "Sense Hat Temperature F": sense_hat_temperature_fehrenheit_rounded,
        "Fan Shim State": fan_sime_sate,
    }

    return data_row_dictionary


def main():
    csv_file_path = Path("/home/pi/raspberry_pi/tools/temperature_log.csv")

    with open(csv_file_path, "a+") as csv_file:
        data_row_dictionary = get_data_row_dictionary()

        headers = list(data_row_dictionary.keys())
        dictionary_writer = csv.DictWriter(csv_file, headers)

        csv_file_is_empty = os.stat(csv_file_path).st_size == 0

        if csv_file_is_empty:
            dictionary_writer.writeheader()

        dictionary_writer.writerow(data_row_dictionary)


if __name__ == "__main__":
    main()
