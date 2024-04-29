import datetime
import pytz
import pandas as pd
import numpy as np
### Here I define functions used in views.py
def return_simulation_time():
    # Here we use UTC time zone
    simulation_start_time = datetime.datetime(2012,7,12,0,0, tzinfo=pytz.utc) # Start time of the simulation, 12th of July 2012
    exercise_start_time = datetime.datetime(2024,4,28,1,0, tzinfo=pytz.utc) # Start time of the ESA SWE Consistent Communications Protocol Campaign exercise
    current_time =  datetime.datetime.now(pytz.utc) # Fetch the current time
    exercise_time_elapsed = current_time-exercise_start_time # How much time has elapsed since the exercise began

    simulated_current_time = simulation_start_time+exercise_time_elapsed # The simulation time that is displayed
    new_datetime_obj = datetime.datetime(simulated_current_time.year, simulated_current_time.month, simulated_current_time.day,
                            simulated_current_time.hour, simulated_current_time.minute, simulated_current_time.second, tzinfo=pytz.utc)
    return new_datetime_obj

def return_event_start_time():
    # Returns time of when the fast CME1 is detected by a coronagraph/radio spectrogram
    event_start = datetime.datetime(2012,7,13,2,40, tzinfo=pytz.utc)
    return event_start