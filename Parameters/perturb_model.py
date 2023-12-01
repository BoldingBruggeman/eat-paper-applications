import eatpy
import numpy as np
N = 50    # ensemble size
with eatpy.models.gotm.YAMLEnsemble("gotm.yaml", N) as gotm, eatpy.models.gotm.YAMLEnsemble("fabm.yaml", N) as fabm:
#    gotm["surface/u10/scale_factor"] = np.random.lognormal(sigma=0.1, size=N)
#    gotm["surface/v10/scale_factor"] = np.random.lognormal(sigma=0.1, size=N)
    gotm["fabm/yaml_file"] = fabm.file_paths
    fabm["instances/P1/parameters/sum"] *= np.random.uniform(low=0.7,high=1.3, size=N)
#    fabm["instances/P1/parameters/xqcn"] *= np.random.uniform(low=0.7,high=1.3, size=N)
#    fabm["instances/P1/parameters/xqn"] *= np.random.uniform(low=0.7,high=1.3, size=N)
#    fabm["instances/P2/parameters/xqcn"] *= np.random.uniform(low=0.7,high=1.3, size=N)
#    fabm["instances/P4/parameters/xqcn"] *= np.random.uniform(low=0.7,high=1.3, size=N)
#    fabm["instances/B1/parameters/pu"] *= np.random.uniform(low=0.7,high=1.3, size=N)
#    fabm["instances/B1/parameters/sR1"] *= np.random.uniform(low=0.7,high=1.3, size=N)
#    fabm["instances/B1/parameters/rR2"] *= np.random.uniform(low=0.7,high=1.3, size=N)
#    fabm["instances/R4/parameters/rm"] *= np.random.uniform(low=0.7,high=1.3, size=N)
