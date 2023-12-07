#!/usr/bin/env python

import numpy as np
import eatpy

N = 20  # ensemble size
gotm = eatpy.models.gotm.YAMLEnsemble("gotm.yaml", N)
fabm = eatpy.models.gotm.YAMLEnsemble("fabm.yaml", N)
with gotm, fabm:
    gotm["surface/u10/scale_factor"] = np.random.lognormal(sigma=0.2, size=N)
    gotm["surface/v10/scale_factor"] = np.random.lognormal(sigma=0.2, size=N)
    gotm["turbulence/turb_param/k_min"] = 5e-6 * np.random.lognormal(sigma=0.3, size=N)
    gotm["fabm/yaml_file"] = fabm.file_paths
    fabm["instances/phy/parameters/mumax0"] *= np.random.lognormal(sigma=0.3, size=N)
    fabm["instances/dia/parameters/mumax0"] *= np.random.lognormal(sigma=0.3, size=N)
