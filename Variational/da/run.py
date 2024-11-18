import datetime
import os
import eatpy
from myPlugins import ogs3dvar_base


# Variables for assimilation
var = "total_chlorophyll"
var_surf = var + "[-1]"

# Observation files
OBSDIR = "../observations"
OBS_FILE_SAT = OBSDIR + "/nrt_chlsat.obs"

# Assimilation period
start = datetime.datetime(2019, 1, 1)
stop = datetime.datetime(2019, 12, 31)


# Set the simulation
experiment = eatpy.models.GOTM(
    diagnostics_in_state=["total_chlorophyll"],
    start=start,
    stop=stop,
)


# Plugins
## select
experiment.add_plugin(
    eatpy.plugins.select.Select(include=("P?_*", "total_chlorophyll", "z"))
)
experiment.add_plugin(ogs3dvar_base.Chl())

## aft bef ouptut
outfile = "DAout.nc"
experiment.add_plugin(eatpy.plugins.output.NetCDF(outfile))


# Observations
experiment.add_observations(var_surf, OBS_FILE_SAT)


# Filter
filter = eatpy.PDAF(eatpy.pdaf.FilterType._3DVar, subtype=0, type_opt=1)


# Run
experiment.run(filter)
