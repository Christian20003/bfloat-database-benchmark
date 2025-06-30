import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Print')))

from datetime import datetime
import subprocess
import Format

def python_time(execution: str) -> float:
    '''
    This function executes the given database command and measures the execution time with
    python tools. This function uses a timeout of 3600 seconds.

    :param execution: The execution command of the database.

    :returns: The measured execution time in seconds or -1 if the timeout has been exceeded.
    '''

    Format.print_information('Start the time benchmark', mark=True)
    start = datetime.now()
    database = subprocess.Popen(
        execution.split(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    try:
        _, error = database.communicate(timeout=3600)
        time = (datetime.now() - start).total_seconds()
        if error:
            Format.print_error('An error has been printed during time benchmark', error)
        return time
    except subprocess.TimeoutExpired:
        database.kill()
        return -1