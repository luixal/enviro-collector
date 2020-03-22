#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Luis Alberto Pérez García <luixal@gmail.com>

import time
from threading import Thread
from enviroplus.noise import Noise

class SoundDetector(Thread):
    def __init__(self, soundLevelToReach, interval, frequency_ranges, onSoundEventCallback):
        self.soundLevelToReach = soundLevelToReach
        self.interval = interval
        self.onSoundEvent = onSoundEventCallback
        self.frequency_ranges = frequency_ranges
        self.noise = Noise()
        # init and start thread:
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def get_noise(self, frequency_ranges):
        amps = self.noise.get_amplitudes_at_frequency_ranges(frequency_ranges)
        return amps

    def is_shouting(self, amps):
        for i in range(len(amps)):
            if amps[i] > self.soundLevelToReach:
                return amps[i]

    def run(self):
        while True:
            amps = self.get_noise(self.frequency_ranges)
            reachedValue = self.is_shouting(amps)
            if reachedValue and self.onSoundEvent:
                self.onSoundEvent(amps, reachedValue)
            time.sleep(self.interval)
