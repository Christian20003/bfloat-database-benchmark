#!/bin/bash
time=$(date +%s)

if [ -d ./kmeans/data ] && [ -d ./kmeans/data/result ]; then
    mv ./kmeans/data/result ./kmeans/data/result_$time
elif [ ! -d ./kmeans/data ]; then
    mkdir ./kmeans/data
fi

if [ -d ./einstein_summation/data ] && [ -d ./einstein_summation/data/result ]; then
    mv ./einstein_summation/data/result ./einstein_summation/data/result_$time
elif [ ! -d ./einstein_summation/data ]; then
    mkdir ./einstein_summation/data
fi

if [ -d ./linear_regression/data ] && [ -d ./linear_regression/data/result ]; then
    mv ./linear_regression/data/result ./linear_regression/data/result_$time
elif [ ! -d ./linear_regression/data ]; then
    mkdir ./linear_regression/data
fi

python3 ./kmeans/KMeans.py -e ../lingo-db/build/lingodb-release -o ../database -f ./kmeans/Statement.sql
mv *.pdf ./kmeans/data/result
mv *.csv ./kmeans/data/result
mv massif.* ./kmeans/data/result

python3 ./einstein_summation/einstein.py -e ../lingo-db/build/lingodb-release -o ../database -f ./einstein_summation/Statement.sql
mv *.pdf ./einstein_summation/data/result
mv *.csv ./einstein_summation/data/result
mv massif.* ./einstein_summation/data/result

python3 ./linear_regression/Regression.py -e ../lingo-db/build/lingodb-release -o ../database -f ./linear_regression/Statement.sql
mv *.pdf ./linear_regression/data/result
mv *.csv ./linear_regression/data/result
mv massif.* ./linear_regression/data/result