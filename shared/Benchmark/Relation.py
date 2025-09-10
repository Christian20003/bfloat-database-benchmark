import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Helper')))

import Format

def measure_relation_size(file_name: str) -> float:
    '''
    This function reads the size of a file.

    :param file_name: The name of the file.

    :returns: The size of the file in bytes.
    '''
    Format.print_information('Read relation size', mark=True)
    return os.path.getsize(file_name)