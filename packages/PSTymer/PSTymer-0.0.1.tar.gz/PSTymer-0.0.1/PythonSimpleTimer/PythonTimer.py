#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Class class controlling the different measures of time
    for a function.

 
    Usage:
 
    >>> PythonSimpleTimer.PythonTimer import PythonTimer
    >>> my_timer = PythonTimer()
    >>> my_timer.start('timer_name')
    >>> -- process stuff --
    >>> my_timer.stop('timer_name')
"""

import time

__all__ = ['PythonTimer']

class PythonTimer:

    def __init__(self):
        self.perf_counter = {}
        self.process_time = {}
        self.cumulated_perf_counter = {}
        self.cumulated_process_time = {}
        self.count = {}

    def start(self, name):
        """
            Start a timer for the tag "name"
        """
        self.perf_counter[name] = time.perf_counter()
        self.process_time[name] = time.process_time()

    def stop(self, name):
        """
            Stop the timer for the tag "name"
        """
        elapsed_perf_counter = (time.perf_counter() - self.perf_counter[name]) * 1000
        elapsed_process_time = (time.process_time() - self.process_time[name]) * 1000
        if name not in self.cumulated_perf_counter:
            self.cumulated_perf_counter[name] = 0
            self.cumulated_process_time[name] = 0
            self.count[name] = 0
        self.cumulated_perf_counter[name] += elapsed_perf_counter
        self.cumulated_process_time[name] += elapsed_process_time
        self.count[name] += 1

    def get_perf_counter_ms(self):
        """
        :return: The time (in ms) between a start and a stop for a timer 
        """
        return self.cumulated_perf_counter

    def get_process_time_ms(self):
        """
        :return: The effective CPU time (in ms) between a start and a stop for a timer 
        """
        return self.cumulated_process_time

    def get_count(self):
        """
        :return: The number of loops in which the timer ran
        """
        return self.count

    def reset(self):
        """
            Resets all the counters (execution time and loops)
        """
        self.perf_counter = {}
        self.cumulated_perf_counter = {}
        self.count = {}
