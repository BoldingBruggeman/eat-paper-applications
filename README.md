# Example applications for the Ensemble and Assimilation Tool (EAT)

These examples can be run on Windows, Mac, or Linux.
They require [Anaconda](https://www.anaconda.com) or [Miniconda](https://docs.conda.io/projects/miniconda/).

All commands below should be executed from a terminal window
(Windows: "Anaconda prompt" in the start menu).

First install [EAT](https://github.com/BoldingBruggeman/eat/wiki). The easiest way to do this is
to create an isolated `eat` environment with the pre-compiled `eatpy` package:

```
conda create -n eat -c bolding-bruggeman -c conda-forge eatpy
```

Then add the Python packages that we will use for post-processing:

```
conda install -n eat -c conda-forge jupyterlab ipympl netcdf4 cmocean scipy
```

To get started with the example applications:

1. Activate the EAT environment by executing `conda activate eat`
2. Open the main notebook by executing `jupyter lab start.ipynb`. The notebook should now open in your browser.
3. Click one of the three examples. In the notebook that opens, execute the cells one by one.
