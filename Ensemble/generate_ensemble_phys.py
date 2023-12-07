#!/usr/bin/env python

import numpy as np
import eatpy
N = 20    # ensemble size
gotm = eatpy.models.gotm.YAMLEnsemble("gotm.yaml", N)
with gotm:
    gotm["surface/u10/scale_factor"] = np.random.lognormal(sigma=0.2, size=N)
    gotm["surface/v10/scale_factor"] = np.random.lognormal(sigma=0.2, size=N)
    gotm["turbulence/turb_param/k_min"] *= np.random.lognormal(sigma=0.2, size=N)
