#!/bin/bash

# Create a conda environment that uses Python 3.11
conda create --name spark332 python=3.11.8
conda activate py311_env
conda install -c conda-forge openjdk=11.0.13
pip install delta-spark==2.3.0 pyspark==3.3.2

# if you want to run in a jupyter notebook
conda install -n spark332 ipykernel --update-deps --force-reinstall
