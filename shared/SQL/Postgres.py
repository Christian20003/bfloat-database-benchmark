import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Print')))

import subprocess
import Format

def create_database(init_exe: str, server_start_exe: str, create_db_exe: str) -> None:
    os.mkdir('./postgres_database')
    init = subprocess.Popen([init_exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, error = init.communicate()
    if (error):
        Format.print_error('Something went wrong during creation of postgres database', error)
    with open('./postgres_database/postgresql.conf', 'a') as file:
        file.write('port = 4444')
    start = subprocess.Popen([server_start_exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, error = start.communicate()
    if (error):
        Format.print_error('Something went wrong during creation of postgres database', error)
    create = subprocess.Popen([create_db_exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, error = create.communicate()
    if (error):
        Format.print_error('Something went wrong during creation of postgres database', error)

def stop_database(server_stop_exe: str) -> None:
    stop = subprocess.Popen([server_stop_exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, error = stop.communicate()
    if (error):
        Format.print_error('Something went wrong during creation of postgres database', error)