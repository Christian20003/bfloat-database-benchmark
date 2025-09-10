import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Print')))

from datetime import datetime
import subprocess
import Format

def python_time(execution: str) -> float:
    '''
    This function executes a time benchmark for a database by executing the provided command.
    For reproducible results, the function sets a timeout of 1 hour. If the timeout is exceeded,
    the function will return -1.

    :param execution: The execution command of the database. This must include an SQL file that 
    the database should execute.

    :returns: The measured execution time in seconds or -1 if the timeout has been exceeded.
    '''

    Format.print_information('Start the time benchmark', mark=True)
    # Measure time
    start = datetime.now()
    # Start the process that should be measured
    database = subprocess.Popen(
        execution.split(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    try:
        _, error = database.communicate(timeout=3600)
        # Calculate the time difference
        time = (datetime.now() - start).total_seconds()
        if error:
            Format.print_error('An error has been printed during time benchmark', error)
        return time
    except subprocess.TimeoutExpired:
        database.kill()
        return -1