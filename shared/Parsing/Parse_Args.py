from typing import Tuple
from pathlib import Path
import argparse

def parse_args() -> Tuple[str, str, str]:
    '''
    This function initializes the arguments for this benchmark file:
        -e:     Path to executable files
        -o:     Path to store persistent data
        -f:     Path of the sql statement which should be benchmarked
    
    :return: A tuple with all three received values
    :raise:  RuntimeError, if invalid paths or empty values are provided 
    '''
    parser = argparse.ArgumentParser('Kmeans', description='Execute Kmeans benchmark on LingoDB')
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
        return (args.executable, args.output, args.file)
    else:
        raise RuntimeError('Missing arguments')