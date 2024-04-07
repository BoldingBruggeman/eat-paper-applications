import numpy as np
import eatpy

rng = np.random.default_rng()

N = 2

# Vary wind speeds (x and y components) and background mixing (minimum turbulent kinetic energy)
gotm = eatpy.models.gotm.YAMLEnsemble("gotm.yaml", N)
with gotm:
    gotm["surface/u10/scale_factor"] = rng.lognormal(mean=0.0, sigma=0.2, size=N)
    gotm["surface/v10/scale_factor"] = rng.lognormal(mean=0.0, sigma=0.2, size=N)
    gotm["turbulence/turb_param/k_min"] *= rng.lognormal(mean=0.0, sigma=0.2, size=N)