#! /bin/bash


rm -f L4_surface_daily_mean_16.06*.nc
rm -f L4_bottom_daily_mean_16.06*.nc
rm -f result*.nc
rm -f restart_????.nc
cp restart_01112014.nc restart.nc

eat-gotm
python perturb_model.py
mpiexec -n 1 python run.py : -n 2 eat-gotm --separate_gotm_yaml
ipython --gui qt -c "%run plot.ipynb"
