# bfloat-database-benchmark
This project is content of a master thesis. The main goal is to analyze the performance of the bfloat (16-bit) datatype in a database system compared with the float datatype. Thereby the execution time and peak heap and rss memory of the database process is collected. The key database in this project is currently DuckDB with implemented features for the bfloat datatype ([DuckDB with bfloat](https://github.com/Christian20003/duckdb/tree/bfloat)).

Currently this project provides the following tasks as benchmark:
1. KMeans (Clustering-Algorithm)
2. Einstein-Summation (Matrix-Multiplication)
3. Gradient-Descent (Simple update with only 2 parameters)
4. Neural-Network (A simple NN with only a single hidden layer, 4 input and 3 output neurons - classification problem)

Currently this project includes the following databases:
1. DuckDB