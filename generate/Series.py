import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from typing import Tuple, List
from threading import Thread, Event
import Config
import Statements
import Settings
import Helper
import Memory
import Format
import Create_CSV
import Database
import subprocess
import psutil
import time

def main():
    databases = Config.CONFIG['databases']
    scenarios = Config.CONFIG['setups']

    for database in databases:
        if database['create_csv'] and not database['ignore']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        entries = scenario['entries']
        for database in databases:
            name = database['name']
            exe = database['memory-executable']
            for type in database['types']:
                for statement in scenario['statements']:
                    Format.print_title(f'START BENCHMARK WITH {name}, {type} AND {entries}')
                    content = statement['statement_duckdb'] if name == 'duckdb' else statement['statement_umbra']
                    generate_statement(content, entries, type)
                    if name == 'umbra':
                        Helper.create_dir(Settings.UMBRA_DIR)
                        prep = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
                        prep.execute_sql()

                    file_name = f'{name}_{type}_{entries}_{statement['array']}'
                    rss_heaptrack = measure_heaptrack(exe, file_name)
                    rss_psuitl, vms_psutil = measure_psutil(exe, entries)

                    Create_CSV.append_row(database['csv_file'], [type, entries, statement['array'], rss_heaptrack, rss_psuitl, vms_psutil])

                    if name == 'umbra':
                        Helper.remove_dir(database['files'])
                    elif name == 'duckdb':
                        Helper.remove_files(database['files'])
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

def measure_psutil(executable: str, rows: int) -> Tuple[float, float]:
    Format.print_information('Start psutil measurement', mark=True)
    event = Event()
    event.set()
    data = []
    sleep = 0.0000001 * rows
    process = subprocess.Popen(
        executable.split(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    process_psutil = psutil.Process(process.pid)
    thread = Thread(target=psutil_thread, args=(event, process_psutil, data, sleep if sleep < 1 else 1))
    thread.start()
    _, error = process.communicate()
    event.clear()
    if error:
        Format.print_error('Catched error during psutil measurement', error)
    thread.join()

    rss_peak = 0
    vms_peak = 0

    for entry in data:
        if entry['rss'] > rss_peak:
            rss_peak = entry['rss']
        if entry['vms'] > vms_peak:
            vms_peak = entry['vms']

    return rss_peak / (1024*1024*1024), vms_peak / (1024*1024*1024)

def psutil_thread(event: Event, process: psutil.Process, data: List, sleep: float) -> None:
    while event.is_set():
        if not process:
            continue
        else:
            try:
                memory = process.memory_info()
                data.append({'rss': memory.rss, 'vms': memory.vms})
                time.sleep(sleep)
            except psutil.NoSuchProcess:
                time.sleep(sleep)
                continue

if __name__ == '__main__':
    main()