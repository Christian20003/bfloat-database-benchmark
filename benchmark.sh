#!/bin/bash
if [ ! -d ./.venv ]; then
    python3 -m venv ./.venv
fi

source .venv/bin/activate

pip install -r requirements.txt

if [ ! -d ./umbra ]; then
    tar -xf umbra.tar.xz
fi

if [ ! -d ./einstein_benchmark ]; then
    mkdir ./einstein_benchmark
fi

if [ ! -d ./gd_benchmark ]; then
    mkdir ./gd_benchmark
fi

if [ ! -d ./iris_benchmark ]; then
    mkdir ./iris_benchmark
fi

cp ./iris.csv ./iris_benchmark

cd ./einstein_benchmark
python ../einstein_summation/Einstein.py

cd ../gd_benchmark
python ../linear_regression/Regression.py

cd ../iris_benchmark
python ../iris_regression/Iris.py