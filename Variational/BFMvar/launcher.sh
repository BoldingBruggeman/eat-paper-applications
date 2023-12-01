#! /bin/bash


rm -f result_0001.nc
rm -f restart_0001.nc
rm -f restart.nc
cp restart20191231_nudgfloat.nc restart.nc
mkdir -p OUTNC

mpiexec -n 1 python runVar.py : -n 1 eat-gotm




