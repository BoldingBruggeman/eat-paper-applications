# Example applications for the Ensemble and Assimilation Tool (EAT)

## Installation

To run these examples, first install [EAT](https://github.com/BoldingBruggeman/eat/wiki).
If you have [Anaconda](https://www.anaconda.com), the easiest way to do this is
by installing a pre-compiled conda package:

```
conda create -n eat -c bolding-bruggeman -c conda-forge eatpy
```

More information about installing EAT, including instructions on how to build
from source, can be found [here](https://github.com/BoldingBruggeman/eat/wiki#installing).

Then add several Python packages used for post-processing:

```
conda install -n eat -c conda-forge jupyterlab ipympl netcdf4 cmocean scipy
```

## Running the applications

Three applications are provided:

* `Ensemble` performs ensemble-based physical and biogeochemical data
  assimilation with the PISCES biogeochemical model at a North Sea site.
* `Variational` performs 3D-Var biogeochemical data assimilation with the
  BFM biogeochemical model at a site in the Mediterranean Sea.
* `Parameters` performs ensemble-based biogeochemical data assimilation to
  estimate a parameter (maximum growth rate of diatoms) of the ERSEM
  biogeochemical model at a site in the Western English Channel.

To run each example application:

1. Go to the application subdirectory (`cd Ensemble`, `cd Variational` or
   `cd Parameters`)
2. Start JupyterLab (`jupyter lab`)
3. Open the notebook `experiment.ipynb`
5. Execute the notebook cell-by-cell

For the `Ensemble` and `Parameters` applications, you can customize the
ensemble size by changing `N` in the first cell.
