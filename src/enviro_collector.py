#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Luis Alberto Pérez García <luixal@gmail.com>

VERSION = '0.1.1'

from os import getenv
import logging

from sound_detector import SoundDetector
from sensors_reader import SensorsReader
from server_sender import ServerSender


logging.basicConfig(
    format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# interval time to read and send values:
interval = float(getenv("INTERVAL", 30.0))
# sound reading interval time to read and send values:
sound_reading_interval = float(getenv("SOUND_READING_INTERVAL", interval))
# sound level threshold??
soundLevelToReach = float(getenv("SOUND_LEVEL_TO_REACH", 0.3))
# temp_compoensation_factor for compensating temperature:
temp_compoensation_factor = float(getenv("TEMP_COMPENSATION_FACTOR", 1.0))
# server url:
server_url = getenv("SERVER_URL", "http://localhost:1880/sensor")
# http basic auth:
http_auth = getenv("HTTP_AUTH")
http_auth_username = getenv("HTTP_AUTH_USERNAME")
http_auth_password = getenv("HTTP_AUTH_PASSWORD")

# logs env values:
messageConfig = "\nENV Values:\n\n"
messageConfig += """  - INTERVAL:\t\t\t\033[1m{}\033[0m\n""".format(interval)
messageConfig += """  - SOUND_READING_INTERVAL:\t\033[1m{}\033[0m\n""".format(sound_reading_interval)
messageConfig += """  - SOUND_LEVEL_TO_REACH:\t\033[1m{}\033[0m\n""".format(soundLevelToReach)
messageConfig += """  - TEMP_COMPENSATION_FACTOR:\t\033[1m{}\033[0m\n""".format(temp_compoensation_factor)
messageConfig += """  - SERVER_URL:\t\t\t\033[1m{}\033[0m\n""".format(server_url)
if (http_auth and http_auth_username and http_auth_password):
    messageConfig += """  - HTTP_AUTH:\t\t\t\033[1m{} | {} | {}\033[0m\n""".format(http_auth, http_auth_username, http_auth_password)

logging.info(messageConfig)

# format value as bold text:
def bold_value(value):
    if type(value) is int:
        return """\033[1m{:05}\033[0m""".format(value)
    else:
        return """\033[1m{:05.2f}\033[0m""".format(value)

# get device info:
def get_device_info():
    info = {}
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if 'Hardware' in line:
                info["Hardware"] = line.split(":")[1].strip()
            if "Revision" in line:
                info["Revision"] = line.split(":")[1].strip()
            if "Serial" in line:
                info["Serial"] = line.split(":")[1].strip()
            if "Model" in line:
                info["Model"] = line.split(":")[1].strip()
    return info
deviceValues = get_device_info()


# returns formatted initial message:
def get_welcome_message():
	message = "\nEnviro Collector \033[1mv{}\033[0m\n\n".format(VERSION)
	for key in deviceValues:
	    message += """  - {}:\t\033[1m{}\033[0m\n""".format(key, deviceValues[key])
	return message

logging.info(get_welcome_message())

# on sound event detected callback:
def onSoundEvent(amps, value):
    print("Sound detected with value {}".format(bold_value(value)))

serverSender = ServerSender(server_url, deviceValues['Serial'], http_auth, http_auth_username, http_auth_password)
# on sensor readings callback:
def onSensorReadings(values):
    temperature = values['temperature']
    temperature_cpu = values['temperature_cpu']
    temperature_compensated = values['temperature_compensated']
    pressure = values['pressure']
    humidity = values['humidity']
    lux = values['light']
    prox = values['proximity']

    message = """Temperature: {} *C | CPU: {} *C | Compensated: {} *C | Pressure: {} hPa | Relative humidity: {} % | Light: {} Lux | Proximity: {}""".format(bold_value(temperature), bold_value(temperature_cpu), bold_value(temperature_compensated), bold_value(pressure), bold_value(humidity), bold_value(lux), bold_value(prox))
    isSent = serverSender.http_send(values)
    if isSent:
    	logging.info(message)
    else:
    	logging.error(message)

# start sound detector:
frequency_ranges = [(100, 200), (500, 600), (1000, 1200)]
SoundDetector(soundLevelToReach, sound_reading_interval, frequency_ranges, onSoundEvent)
# start sensors reader:
SensorsReader(interval, temp_compoensation_factor, onSensorReadings)

while True:
    pass
