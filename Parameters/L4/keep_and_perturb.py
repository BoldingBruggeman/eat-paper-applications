from typing import Mapping, Any
import eatpy.shared
import numpy as np
import datetime

# state variables that the DA scheme is allowed to manipulate
#kept_vars = ["temp", "salt", "P1_chl", "P2_chl", "P3_chl", "P4_chl"]
#kept_vars = ["P1_Chl", "P2_Chl", "P3_Chl", "P4_Chl", "P1_c", "P1_n", "P1_p", "P1_s", "P2_c", "P2_n", "P2_p", "P3_c", "P3_n", "P3_p", "P4_c", "P4_n", "P4_p", "instances_B1_parameters_rR2"]
kept_vars = ["P1_Chl", "P1_c", "P1_p", "P1_n", "P1_s"]
#kept_vars = ["P3_Chl"]
#kept_vars = ["P2_Chl", "P2_c", "P2_p", "P2_n", "instances_P2_parameters_xqn", "instances_P2_parameters_xqcn"]

list_positive=kept_vars

# state variables that need to be log-transformed
#logtransformed_vars = ["P2_Chl", "P3_Chl", "P1_Chl", "P4_Chl"]
logtransformed_vars = []
#logtransformed_vars = kept_vars
#temp_free = np.zeros((365,100))
#perturbed_vars = ["instances_P1_parameters_xqn", "instances_P1_parameters_xqcn", "instances_P1_parameters_sum"]

perturbed_vars = ["instances_P2_parameters_xqn", "instances_P2_parameters_xqcn"]


clip_below=True
tresh_below=0.1

clip_above=True
tresh_above = 5.


class MyPlugin(eatpy.shared.Plugin):
    def initialize(self, variables: Mapping[str, Any], ensemble_size: int):
        self.logvars = []
        self.perturbvars = []
        self.vars = variables
        for name in list(variables):
            if name not in kept_vars:
                del variables[name]
            elif name in logtransformed_vars:
                self.logvars.append(variables[name])
            elif name in perturbed_vars:
                self.perturbvars.append(variables[name])

    def before_analysis(self, time: datetime.datetime, state: np.ndarray, iobs: np.ndarray, obs: np.ndarray, obs_sds: np.ndarray, filter: eatpy.shared.Filter):
        for info in self.logvars:
            start, stop = info["start"], info["stop"]
            affected_obs = (iobs >= start) & (iobs < stop)
            if affected_obs.any():
                obs[affected_obs] = np.log10(obs[affected_obs])
            info["data"][...] = np.log10(info["data"])
               
#        for info in self.perturbvars:
#            start, stop = info["start"], info["stop"]
#            affected_obs = (iobs >= start) & (iobs < stop)

#            if (clip_below) & (np.mean(info["data"][:,-1]) < tresh_below):
#                info["data"][:,-1] += tresh_below - np.mean(info["data"][:,-1])
#                cond = info["data"][:,-1] < 0.2*tresh_below
#                info["data"][cond,-1] = 0.2*tresh_below
#            elif (clip_above) & (np.mean(info["data"][:,-1]) > tresh_above):
#                info["data"][:,-1] -= np.mean(info["data"][:,-1]) - tresh_above
#                info["data"][:,-1] = min(info["data"][:,-1], 10*tresh_above)
#                cond = info["data"][:,-1] > 5.*tresh_below
#                info["data"][cond,-1] = 5.*tresh_below



#                if n_faulty>0:
#                    info["data"][cond,-1] = np.random.uniform(tresh-0.1*tresh, tresh+0.1*tresh, size=n_faulty)
#            if affected_obs.any():
#                obs[affected_obs] = max(obs[affected_obs] + np.random.normal(loc=0.0, scale = 0.25*obs[affected_obs], size=1), 0.)
#            print("IMPOOOOOOOOOOOOOOOOOOOOOORTANT", np.shape(info["data"]))

            

#            if len(np.shape(info["data"]))==2:
#                ens_position_surface = info["data"][:,-1] - np.mean(info["data"][:,-1])   # what is the mean spread between ens mem at the surface
#                if np.mean(np.abs(ens_position_surface)) < 0.15*np.mean(info["data"][:,-1]):  # if it's less than 15% of the mean then inflate it to 15%
#                    print("Increasing spread of the ensemble")   
#                    for depth in range(0,np.shape(info["data"])[1]):
#                        ens_position = info["data"][:,depth] - np.mean(info["data"][:,depth])    # at each depth find the member position relative to the mean 
#                        coeff =  0.15*(np.mean(np.abs(ens_position))/np.mean(np.abs(ens_position_surface)))*np.mean(info["data"][:,depth])/np.mean(np.abs(ens_position))  # this inflates each member to the distance that on average will be N% of the mean, where N scales with depth as the ensemble spread... At the surface by definition N=15.
#                        for mem in range(0,np.shape(info["data"])[0]):
#                            info["data"][mem,depth] = np.mean(info["data"][:,depth]) + coeff*ens_position[mem]   # inflation step
#            elif len(np.shape(info["data"]))==1:
#                ens_position_surface = info["data"] - np.mean(info["data"])   # what is the mean spread between ens mem at the surface
#                if np.mean(np.abs(ens_position_surface)) < 0.15*np.mean(info["data"]):  # if it's less than 15% of the mean then inflate it to 15%
#                    print("Increasing spread of the ensemble")
#                    coeff =  0.15*np.mean(info["data"])/np.mean(np.abs(ens_position_surface))
#                    for mem in range(0,np.shape(info["data"])[0]):
#                        info["data"][mem] = np.mean(info["data"]) + coeff*ens_position_surface[mem]   # inflation step


    def after_analysis(self, state: np.ndarray):
        for info in self.logvars:
            info["data"][...] = 10. ** info["data"]

        SMALL=1.0e-8

        for info in self.perturbvars:
            start, stop = info["start"], info["stop"]
#            affected_obs = (iobs >= start) & (iobs < stop)

            if (clip_below) & (np.mean(info["data"][:,-1]) < tresh_below):  # if you want to clip the mean of the par distribution from below
                info["data"][:,-1] += tresh_below - np.mean(info["data"][:,-1])
                cond = info["data"][:,-1] < 0.2*tresh_below
                info["data"][cond,-1] = 0.2*tresh_below
            elif (clip_above) & (np.mean(info["data"][:,-1]) > tresh_above):   # if you want to clip the mean of the par distribution from above
                info["data"][:,-1] -= np.mean(info["data"][:,-1]) - tresh_above
#                info["data"][:,-1] = min(info["data"][:,-1], 10*tresh_above)
                cond = info["data"][:,-1] > 5.*tresh_below
                info["data"][cond,-1] = 5.*tresh_below



#                if n_faulty>0:
#                    info["data"][cond,-1] = np.random.uniform(tresh-0.1*tresh, tresh+0.1*tresh, size=n_faulty)
#            if affected_obs.any():
#                obs[affected_obs] = max(obs[affected_obs] + np.random.normal(loc=0.0, scale = 0.25*obs[affected_obs], size=1), 0.)
#            print("IMPOOOOOOOOOOOOOOOOOOOOOORTANT", np.shape(info["data"]))



            if len(np.shape(info["data"]))==2:
                ens_position_surface = info["data"][:,-1] - np.mean(info["data"][:,-1])   # what is the mean spread between ens mem at the surface
                if np.mean(np.abs(ens_position_surface)) < 0.15*np.mean(info["data"][:,-1]):  # if it's less than 15% of the mean then inflate it to 15%
                    print("Increasing spread of the ensemble")
                    for depth in range(0,np.shape(info["data"])[1]):
                        ens_position = info["data"][:,depth] - np.mean(info["data"][:,depth])    # at each depth find the member position relative to the mean 
                        coeff =  0.15*(np.mean(np.abs(ens_position))/np.mean(np.abs(ens_position_surface)))*np.mean(info["data"][:,depth])/np.mean(np.abs(ens_position))  # this inflates each member to the distance that on average will be N% of the mean, where N scales with depth as the ensemble spread... At the surface by definition N=15.
                        for mem in range(0,np.shape(info["data"])[0]):
                            info["data"][mem,depth] = np.mean(info["data"][:,depth]) + coeff*ens_position[mem]   # inflation step
            elif len(np.shape(info["data"]))==1:
                ens_position_surface = info["data"] - np.mean(info["data"])   # what is the mean spread between ens mem at the surface
                if np.mean(np.abs(ens_position_surface)) < 0.15*np.mean(info["data"]):  # if it's less than 15% of the mean then inflate it to 15%
                    print("Increasing spread of the ensemble")
                    coeff =  0.15*np.mean(info["data"])/np.mean(np.abs(ens_position_surface))
                    for mem in range(0,np.shape(info["data"])[0]):
                        info["data"][mem] = np.mean(info["data"]) + coeff*ens_position_surface[mem]   # inflation step


        for name in self.vars:
            start=self.vars[name]['start']
            stop=start + self.vars[name]['length']
            var = state[:, start:stop]  # note: the first axis is for the ensemble members
            if name in list_positive:
                print("Number of negative values: ", len(var[var<0]))
                var[var<0] = SMALL
