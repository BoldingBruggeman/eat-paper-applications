# Example applications for the Ensemble and Assimilation Tool (EAT)

To run these examples, first install [EAT](https://github.com/BoldingBruggeman/eat/wiki). If you have [Anaconda](https://www.anaconda.com), the easiest way to do this is by installing a pre-compiled conda package:
```
conda create -n eat -c bolding-bruggeman -c conda-forge eatpy
```

More information about installing EAT, including instructions on how to build from source, can be found [here](https://github.com/BoldingBruggeman/eat/wiki#installing).

Then add several Python packages used for post-processing:

```
conda install -n eat -c conda-forge jupyterlab ipympl netcdf4 cmocean scipy
```

## Coupled physical-biogeochemical state estimation with ensemble-based assimilation

To run this example:

1. go to the `Ensemble` subdirectory (`cd Ensemble`)
2. start JupyterLab (`jupyter lab`)
3. open the notebook `experiment.ipynb`
4. customize the ensemble size as desired (`N` in the first cell), then execute the notebook cell-by-cell

## Biogeochemical state estimation with variational assimilation

To run this example:

1. Perform a free run by executing `eat-gotm` in the `Variational/BFM` subdirectory:
   ```
   cd Variational/Free
   eat-gotm
   ```
   (go back up the directory tree with `cd ../..`)

2. Perform the data assimilation experiment:
   ```
   cd Variational/BFMvar
   mkdir -p OUTNC
   mpiexec -n 1 python runVar.py : -n 1 eat-gotm
   ```
   (go back up the directory tree with `cd ../..`)

2. Create the figures (currently Linux/Mac only):
   ```
   cd Variational/FiguresScripts
   ./launcher.sh
   ```

## Parameter estimation with ensemble-based assimilation

To run this example:

1. Enter the `Parameters` subdirectory (`cd Parameters`)
2. Copy the initial state from `restart_01112014.nc` (Linux/Mac: `cp restart_01112014.nc restart.nc`, Windows: `copy restart_01112014.nc restart.nc`)
3. Perform a free run by executing `eat-gotm`. NB after this completes, `restart.nc` contains the model state at the end of the free run.
4. Create the ensemble: `python perturb_model.py`
5. Copy the initial state from `restart_01112014.nc` (Linux/Mac: `cp restart_01112014.nc restart.nc`, Windows: `copy restart_01112014.nc restart.nc`)
6. Perform the data assimilation experiment: `mpiexec -n 1 python run.py : -n 50 eat-gotm --separate_gotm_yaml`
7. Start JupyterLab (`jupyter lab`)
8. Open the notebook `plot.ipynb`
9. Execute the notebook cell-by-cell
