#! bin/bash

python3 ./kmeans/KMeans.py -e ../lingo-db/build/lingodb-release -o ../database -f ./kmeans/Statement.sql
mkdir ./kmeans/data
mv *.pdf ./kmeans/data
mv *.csv ./kmeans/data
mv massif.* ./kmeans/data

python3 ./einstein_summation/einstein.py -e ../lingo-db/build/lingodb-release -o ../database -f ./einstein_summation/Statement.sql
mkdir ./einstein_summation/data
mv *.pdf ./einstein_summation/data
mv *.csv ./einstein_summation/data
mv massif.* ./einstein_summation/data

python3 ./linear_regression/Regression.py -e ../lingo-db/build/lingodb-release -o ../database -f ./linear_regression/Statement.sql
mkdir ./linear_regression/data
mv *.pdf ./linear_regression/data
mv *.csv ./linear_regression/data
mv massif.* ./linear_regression/data