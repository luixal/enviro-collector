#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Luis Alberto Pérez García <luixal@gmail.com>

import time
from threading import Thread

from bme280 import BME280
from ltr559 import LTR559

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
ltr559 = LTR559()

class SensorsReader(Thread):
    def __init__(self, interval, temp_compoensation_factor, onNewReadingsEventCallback):
        self.interval = interval
        self.temp_compoensation_factor = temp_compoensation_factor
        self.onNewReadingsEventCallback = onNewReadingsEventCallback
        # init and start thread:
        Thread.__init__(self)
        self.daemon = True
        self.start()

    # get CPU temperature:
    def get_cpu_temperature(self):
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000.0
        return temp

    # get compensated temperature:
    def get_compensated_temperature(self):
        cpu_temps = [self.get_cpu_temperature()] * 5
        cpu_temp = self.get_cpu_temperature()
        # Smooth out with some averaging to decrease jitter
        cpu_temps = cpu_temps[1:] + [cpu_temp]
        avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
        raw_temp = bme280.get_temperature()
        comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / self.temp_compoensation_factor)
        return comp_temp

    # get all values from sensors:
    def get_sensor_values(self):
        return {
            "temperature": bme280.get_temperature(),
            "temperature_cpu": self.get_cpu_temperature(),
            "temperature_compensated": self.get_compensated_temperature(),
            "pressure": bme280.get_pressure(),
            "humidity": bme280.get_humidity(),
            "light": ltr559.get_lux(),
            "proximity": ltr559.get_proximity()
        }

    def run(self):
        while True:
            # callback!
            self.onNewReadingsEventCallback(self.get_sensor_values())
            time.sleep(self.interval)
