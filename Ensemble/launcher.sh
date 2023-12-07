#! /bin/bash


rm -f *.nc

eat-gotm

python generate_ensemble_phys.py
mpiexec -n 1 python assimilate_sst.py : -n 2 eat-gotm --separate_gotm_yaml
ipython --gui qt -c "%run analyze_sst_da.ipynb"

python generate_ensemble_phys_bgc.py
mpiexec -n 1 python assimilate_sst_chl.py : -n 2 eat-gotm --separate_gotm_yaml
ipython --gui qt -c "%run analyze_sst_chl_da.ipynb"
