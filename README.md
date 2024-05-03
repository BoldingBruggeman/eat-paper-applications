# Example applications for the Ensemble and Assimilation Tool (EAT)

These examples can be run on Windows, Mac, or Linux.
They require [Anaconda](https://www.anaconda.com) or
[Miniconda](https://docs.conda.io/projects/miniconda/).

All commands below should be executed from a terminal window
(Windows: "Anaconda prompt" in the start menu).

## Installation

First install [EAT](https://github.com/BoldingBruggeman/eat/wiki). The easiest
way to do this is to create an isolated `eat` environment with the pre-compiled
`eatpy` package:

```
conda create -n eat -c conda-forge eatpy
```

Then add the Python packages that we will use for post-processing:

```
conda install -n eat -c conda-forge jupyterlab ipympl netcdf4 cmocean scipy
```

## Running the experiments

To get started with the example applications:

1. Activate the EAT environment by executing `conda activate eat`
2. Open JupyterLab by executing `jupyter lab`. The JupyterLab environment
   should now open in your browser.
3. Within JupyterLab, open the `start.ipynb` notebook.
4. Click one of the three examples. In the notebook that opens, execute the
   cells one by one.

## Provided files

Each application directory contains the following:

* `experiment.ipynb`: the Jupyter Notebook that runs the experiment
* `reference`: a directory with the physical and biogeochemical configuration
  for the reference (free running) simulation
* `forcing`: a directory with forcing files (e.g., meteorology) used by all
  simulations
* `observations`: a directory with observations to assimilate
* `da*`: one or more directories with run scripts for data assimilation
  experiments