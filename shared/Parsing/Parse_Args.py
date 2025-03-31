from typing import Dict
from pathlib import Path
import argparse

def parse_args(process_name: str) -> Dict:
    '''
    This function process the provided arguments for this benchmark:
        -e:     Path to the executable files
        -o:     Path to the persistent storage
        -f:     Path of the sql statement which should be benchmarked
    The resulting dictionary contains the following content:
        "exe":          Path to the sql executable of LingoDB
        "exe_bench":    Path to the run-sql executable of LingoDB
        "storage":      Path to the persistent storage directory
        "statement":    Path to the statement file
    :param process_name: The name of the process which is executed
    
    :return: A dictionary with all received arguments
    :raise:  RuntimeError, if invalid paths or empty values are provided 
    '''
    parser = argparse.ArgumentParser('[File name]', description=f'Execute a {process_name} benchmark on LingoDB')
    parser.add_argument('-e', '--executable', type=str, help='Path to the executables', required=True)
    parser.add_argument('-o', '--output', type=str, help='Path to store tables', required=True)
    parser.add_argument('-f', '--file', type=str, help='File with the SQL statement to benchmark', required=True)
    args = parser.parse_args()
    # Proof if arguments exists
    if args.executable and args.output and args.file:
        sql_exe = Path(f'{args.executable}/sql')
        run_sql_exe = Path(f'{args.executable}/run-sql')
        output_path = Path(args.output)
        file = Path(args.file)
        # Proof if directories and files exists
        if not sql_exe.exists():
            raise RuntimeError(f'{sql_exe.__str__()} not found')
        if not run_sql_exe.exists():
            raise RuntimeError(f'{run_sql_exe.__str__()} not found')
        if not output_path.exists():
            raise RuntimeError(f'{output_path.__str__()} does not exist')
        if not file.exists():
            raise RuntimeError(f'{file.__str__()} does not exist')
        return {
            'exe': args.executable + '/sql',
            'exe_bench': args.executable + '/run-sql',
            'storage': args.output,
            'statement': args.file
        }
    else:
        raise RuntimeError('Missing arguments')