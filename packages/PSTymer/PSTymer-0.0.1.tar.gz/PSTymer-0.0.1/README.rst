python-simple-timer - Monitor time for Python code.
========================================================

This module allows to monitor time for Python code.
You can tag different timers and know how long each of them took and, 
if they were in a loop, how many loops the ran into.


You can install it with pip:

    pip install pstymer

Usage:

    >>> PythonSimpleTimer.PythonTimer import PythonTimer
    >>> my_timer = PythonTimer()
    >>> my_timer.start('timer_name')
    >>> -- process stuff --
    >>> my_timer.stop('timer_name')