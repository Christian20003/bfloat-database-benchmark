# Bfloat Database Benchmark

## Description
This repository contains the content of a master's thesis focused on analyzing the performance of the bfloat datatype in comparison to the traditional float and double types in databases. The primary objective of this project is to provide a comprehensive evaluation of how bfloat performs across various computational tasks in context of in database machine learning. Bfloat has been implemented in two databases, DuckDB and LingoDB. Due to its reduced precision, bfloat has a known rounding problem. Therefore, this project also includes Kahan summation.

## Metrics
These are the following metrics that will be measured:
1. **Execution Time**: The time to complete a provided SQL statement (in seconds).
2. **Memory**: The memory consumption peak during the execution of the provided SQL statement (in bytes).
3. **Relation Size**: The size of the output relation except for the neural network, where the weight relation is measured (in bytes).
4. **Accuracy**: Either the mean absolute percentage error (MAPE) or the prediction accuracy of the neural network (in percent).

## Executed Tasks
These are the following tasks that will be measured:
1. **Einstein Summation**: Executing matrix multiplication with two matrices (as well as one matrix) and a vector.
2. **Gradient Descent**: Train a model to solve a linear regression problem with two to ten parameters.
3. **Neural Network**:  Train a neural network to classify flowers based on four different attributes (from https://github.com/Apaulgithub/oibsip_taskno1)

## Databases
These are the following databases that are executed:
1. **DuckDB**: A modern database system that is able to run entirely on main memory and relies on the vectorized execution paradigm.
2. **LingoDB**: A modern database system that is able to run entirely on main memory and relies on the data-centric code generation paradigm. Thereby, the MLIR compiler technology is used.
3. **Umbra**: A modern database system that is able to run entirely on main memory and relies on the data-centric code generation paradigm.
4. **PostgreSQL**: A traditional database system that depends on persistent memory and is designed with a client-server architecture.

## Execution Steps

### Important requirements
These benchmarks have been executed on a powerful machine with the following specifications:

1. CPU: Intel Xeon W-2295
2. RAM: 125 GB
3. Persistent Storage: More than 100 GB.

Make sure you have enough RAM and persistent storage; otherwise, the operating system will cancel the benchmarks. 

### Database preparations

Before executing the shell script to start the benchmarks, some databases need to be installed.

#### DuckDB
1. Clone the repository (from https://github.com/Christian20003/duckdb) and switch to the correct branch.
```bash
git clone https://github.com/Christian20003/duckdb.git
cd duckdb
git checkout list_arithmetic
```
2. (Optional) If the Ninja build system is installed, make sure the necessary flag is set.
```bash
export GEN=ninja
```
3. Create the executable of DuckDB.
```bash
make release
```

#### LingoDB
1. Clone the repository (from https://gitlab.studium.uni-bamberg.de/christian-matthias.goellner/lingo-db) and switch to the correct branch.
```bash
git clone https://gitlab.studium.uni-bamberg.de/christian-matthias.goellner/lingo-db.git
cd lingo-db
git checkout benchmarkv2.0
```
2. Create the executables of LingoDB.
```bash
make build-release
```

#### PostgreSQL
1. Clone the repository (from https://github.com/postgres/postgres).
```bash
git clone https://github.com/postgres/postgres.git
cd postgres
```
2. Create the executables of PostgreSQL. In the third command, please add the absolute path to the release directory.
```bash
mkdir Release
cd Release
../configure --prefix=<absolute_path_to_Release>
make
make install
```

#### Umbra
This database is included in the repository. If you have access to Umbra's source code, you can use it as well. 

### Starting Benchmarks

1. Clone this repository
 ```bash
git clone https://github.com/Christian20003/bfloat-database-benchmark.git
cd bfloat-database-benchmark
```
2. Ensure that the absolute paths of the databases in the file <code>./shared/Global/Settings.py</code> are correct.
3. Execute the script
 ```bash
./benchmark.sh
```

You can also run certain benchmarks by yourself. However, further steps are required.

1. (Optional) If the <code>benchmark.sh</code> file has not already created the virtual Python environment, you must do so manually. 
 ```bash
python3 -m venv ./.venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. (Optional) If the <code>benchmark.sh</code> file has not already unpack Umbra and you do not want to use your version, you must do so manually.
 ```bash
tar -xf umbra.tar.xz
```
3. After activating the virtual Python environment, execute the desired Python script. Note that all generated files will be stored in the directory in which the script is executed. Here for example with Einstein summation
 ```bash
python ./einstein_summation/Einstein.py
```

## Configurations

Each benchmark allows for custom configurations, which are stored in their corresponding <code>Config.py</code> file. 

### Einstein Summation
* <code>memory_trials</code>: Defines how many times the memory should be measured to calculate a mean. If <code>memory_average</code> is set to <code>false</code> this value determines how many times a measurement should be taken until a valid result is obtained. In rare cases unfortunately, the result is negativ.
* <code>memory_average</code>: Defines whether a mean value should be calculated or if the first valid value should be selected.
* <code>setup</code>: Stores a list of scenarios that should be executed (Can be extended)
    * <code>id</code>: The ID of the scenario in written form.
    * <code>dimension</code>: The size of a single dimension of a tensor (Matrix and Vector).
    * <code>ignore</code>: If this specific scenario should be ignored.
    * <code>statements</code>: The SQL statements that should be executed within this scenario.

### Gradient Descent
* <code>memory_trials</code>: Defines how many times the memory should be measured to calculate a mean. If <code>memory_average</code> is set to <code>false</code> this value determines how many times a measurement should be taken until a valid result is obtained. In rare cases unfortunately, the result is negativ.
* <code>memory_average</code>: Defines whether a mean value should be calculated or if the first valid value should be selected.
* <code>param_value</code>: The true value of each parameter.
* <code>param_start</code>: The initial value of each parameter in the model.
* <code>setup</code>: Stores a list of scenarios that should be executed (Can be extended)
    * <code>iterations</code>: The number of iterations that should be performed. 
    * <code>lr</code>: The learning rate that should be used.
    * <code>ignore</code>: If this specific scenario should be ignored.
    * <code>statement</code>: The SQL statement that should be executed within this scenario.
    * <code>points_amount</code>: The number of points that should be used for model training.
    * <code>params_amount</code>: The number of parameters that are used to make predictions. Must be compatible with the SQL statement in <code>statement</code>.

### Neural Network (Iris)
* <code>memory_trials</code>: Defines how many times the memory should be measured to calculate a mean. If <code>memory_average</code> is set to <code>false</code> this value determines how many times a measurement should be taken until a valid result is obtained. In rare cases unfortunately, the result is negativ.
* <code>memory_average</code>: Defines whether a mean value should be calculated or if the first valid value should be selected.
* <code>learning_rate</code>: The learning rate that should be used.
* <code>setup</code>: Stores a list of scenarios that should be executed (Can be extended)
    * <code>iterations</code>: The number of iterations that should be performed. 
    * <code>ignore</code>: If this specific scenario should be ignored.
    * <code>network_size</code>: The number of neurons in the hidden layer.
    * <code>data_size</code>: The number of samples used for model training.
    * <code>statements</code>: The SQL statements that should be executed within this scenario.
        * <code>statement</code>: The SQL statement which returns the accuracy at each iteration.
        * <code>weights</code>: The SQL statement which returns all weights at each iteration.

### Databases
Databases can also be configured, which can be found in <code>./shared/Global/</code>. But only change the options mentioned below.

* <code>ignore</code>: If this specific database should be ignored.
* <code>csv_file</code>: The name of the CSV file containing all results of a specific database for a certain benchmark.
* <code>types</code>: A list of datatypes that should be used for the benchmarks.
* <code>aggregations</code>: A list of aggregation functions that should be used for the benchmarks. *Standard* refers to ordinary aggregation functions (<code>SUM</code> and <code>AVG</code>), whereas *Kahan* refers to aggregation functions including Kahan summation.

### Memory Measurement

This project also includes a function that uses the <code>heaptrack</code> tool to measure memory. Ensure that this tool is installed on your system. If you want to use it, you have to change some code in <code>./einstein_summation/Einstein.py</code>, <code>./linear_regression/Regression.py</code> and  <code>./iris_regression/Iris.py</code>. Comment out the following code block:
 ```python
for idx in range(CONFIG['memory_trials']):
# It seems to be that with umbra and lingodb the original approach does not work correctly
if name == 'umbra' or name == 'lingodb':
    memory = Memory.python_memory(time_exe, time)
else:
    memory = Memory.python_memory(memory_exe, time, query)
# Make measurement multiple times if selected
if CONFIG['memory_average']:
    memory_state.append(memory[0] if memory[0] > 0 else 0) 
    Format.print_information(f'{idx+1}. Measurement')
else:
    # If psutil does not catch memory correctly, try again
    if memory[0] > 0:
        memory_state.append(memory[0]) 
        break
    else:
        Format.print_information('Did not measure a correct value. Try again')
```

Replace it with the following function call:

 ```python
memory_state.append(Memory.heaptrack_memory(time_exe, <file_name>))
```

The second parameter must be a string that defines the name of the file to be generated through <code>heaptrack</code>.

### Plots

Each benchmark directory includes a <code>Plot.py</code> file that can be executed to generated plots of the results. If you want to use it, make sure that the paths for the results CSV files are correct.