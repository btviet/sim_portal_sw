import datetime
import pytz

from simulation_functions import return_simulation_time, return_event_start_time

def time_context(request):
    time = return_simulation_time
    return {'time': time}

def event_context(request):
    event_start = return_event_start_time
    return {'eventstart': event_start}