import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from typing import Tuple
from threading import Thread
import Config
import Statements
import Settings
import Helper
import Memory
import Format
import Create_CSV
import subprocess
import psutil
import time

PSUTIL_DATA = []
PSUITL_PROCESS: psutil.Process = None
PSUTIL_RUN = True

def main():
    databases = Config.CONFIG['databases']
    scenarios = Config.CONFIG['setups']

    for database in databases:
        if database['create_csv'] and not database['ignore']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        for database in databases:
            for type in database['types']:
                generate_statement(Statements.STATEMENT, scenario['rows'], type)

                file_name = f'{database["name"]}_{type}_{scenario["rows"]}'
                rss_heaptrack = measure_heaptrack(database['memory-executable'], file_name)
                rss_psuitl, vms_psutil = measure_psutil(database['memory-executable'])

                Create_CSV.append_row(database['csv_file'], [type, scenario['rows'], rss_heaptrack, rss_psuitl, vms_psutil])

                if database['name'] == 'umbra':
                    Helper.remove_dir(Settings.UMBRA_DIR)
                elif database['name'] == 'duckdb':
                    Helper.remove_files([Settings.DUCK_DB_DATABASE_FILE])
    Helper.remove_files([Settings.STATEMENT_FILE])


def generate_statement(statement: str, rows: int, type: str) -> None:
    with open(Settings.STATEMENT_FILE, 'w') as file:
        file.write(statement.format(type, rows))

def measure_heaptrack(executable: str, file_name: str) -> float:
    Format.print_information('Start heaptrack measurement', mark=True)
    process = subprocess.Popen(
        ['heaptrack', '-o', file_name] + executable.split(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    _, error = process.communicate()
    if error:
        Format.print_error('Catched error during heaptrack measurement', error)

    Format.print_information('Start heaptrack output parsing', mark=True)
    _, rss = Memory.parse_output('dummy', file_name)
    return rss

def measure_psutil(executable: str) -> Tuple[float, float]:
    thread = Thread(target=psutil_thread)
    thread.start()
    process = subprocess.Popen(
        executable.split(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    PSUITL_PROCESS = psutil.Process(process.pid)
    _, error = process.communicate()
    PSUTIL_RUN = False
    if error:
        Format.print_error('Catched error during psutil measurement', error)
    thread.join()

    rss_peak = 0
    vms_peak = 0

    for entry in PSUTIL_DATA:
        if entry['rss'] > rss_peak:
            rss_peak = entry['rss']
        if entry['vms'] > vms_peak:
            vms_peak = entry['vms']

    return rss_peak / (1024*1024), vms_peak / (1024*1024)

def psutil_thread() -> None:
    while PSUTIL_RUN:
        if not PSUITL_PROCESS:
            continue
        else:
            memory = PSUITL_PROCESS.memory_info()
            PSUTIL_DATA.append({'rss': memory.rss, 'vms': memory.vms})
            time.sleep(1)

if __name__ == '__main__':
    main()