import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Global')))

import subprocess
import Settings
import Format

def create_database(init_exe: str, server_start_exe: str, create_db_exe: str) -> None:
    init = subprocess.Popen(init_exe.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, error = init.communicate()
    if (error):
        Format.print_error('Postgres printed an error on database initialisation', error)
    with open(f'{Settings.POSTGRESQL_DIR}/postgresql.conf', 'a') as file:
        file.write(f'port = {Settings.POSTGRESQL_PORT}')
    start = subprocess.Popen(server_start_exe.split())
    _, error = start.communicate()
    create = subprocess.Popen(create_db_exe.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, error = create.communicate()
    if (error):
        Format.print_error('Postgres printed an error on database creation', error)

def stop_database(server_stop_exe: str) -> None:
    stop = subprocess.Popen(server_stop_exe.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, error = stop.communicate()
    if (error):
        Format.print_error('Postgres printed an error on database shutdown', error)