import eatpy.filter
import numpy as np
import logging
import datetime
#from my_plugins.IO import readtxt
from typing import MutableMapping, Any, Optional#, Dict
from collections import OrderedDict
#from scipy import interpolate

import sys

class Chl(eatpy.pdaf.CvtHandler):
    
    # def __init__(self, dim_cvec=26, dim_cvec_ens=3, eofs_filestring: str = 'data/init/eof.', z_file: str = 'data/init/z.txt', name: str = 'OGS-3Dvar'):
    # def __init__(self, dim_cvec: Optional[int] = None, dim_cvec_ens: Optional[int] = None, eofs_filestring: str = 'data/init/eof.', z_file: str = 'data/init/z.txt', name: str = 'OGS-3Dvar'):
    def __init__(self, dim_cvec: Optional[int] = None, dim_cvec_ens: Optional[int] = None, eofs_filestring: str = '../data/init/eof.', z_file: str = '../data/init/z.txt', name: str = 'OGS-3Dvar'):
        super().__init__(dim_cvec,dim_cvec_ens)
        self.dim_cvec=26
        self.logger = logging.getLogger(name)
        self.eofs_filestring=eofs_filestring
        self.z_file=z_file

    def initialize(self, variables: MutableMapping[str, Any], ensemble_size: int):
        # Here you might add routines that read the square root of the error covariance matrix (Vmat_p) from file
        self.month = -1
        
        self.logger.info('Initialization')
        
        self.logger.info('Available variables: {}'.format(', '.join(variables)))
        
        self.variables = variables
        self.pvars = [variable for variable in variables.keys() if variable[0]=='P']
        self.chlvars = [variable for variable in self.pvars if variable[-3:]=='Chl']
        self.allvars = self.pvars

        self.nz = self.variables['z']['length']
            
        self.logger.info('Reading z levels from file: {}'.format(self.z_file))
        self.z_eof=np.loadtxt(self.z_file)
        self.nz_eof=self.z_eof.size
        
        # self.logger.info('Reading EOFs from file: {}'.format(self.eofs_file))
        # self.Vmat_p = readtxt(self.eofs_file, [self.dim_cvec, self.nz])
        # self.Vmat_p = self.Vmat_p[:,::-1]
        
        self.logger.info('Initialized')
    
    def before_analysis(
        self,
        time: datetime.datetime,
        state: np.ndarray,
        iobs: np.ndarray,
        obs: np.ndarray,
        obs_sds: np.ndarray,
        filter: eatpy.shared.Filter
        ):
        

        if time.month!=self.month:
            self.month = time.month

            self.eofs_file = f'{self.eofs_filestring}{self.month:02d}.txt'
            # self.eofs_file = se initlf.eoffilestring + ('%02d' %self.month)
            self.logger.info('Reading EOFs from file: {}'.format(self.eofs_file))
            # eofs = readtxt(self.eofs_file, [self.dim_cvec, self.nz_eof])
            eofs = np.loadtxt(self.eofs_file)
            
            #f = interpolate.interp1d(-self.z_eof[::-1],eofs[:,::-1],
            #                        fill_value=(eofs[:,-1],eofs[:,0]),
            #                        bounds_error=False,
            #                        assume_sorted=True,
            #                        copy=False,
            #                        )

            self.Vmat_p = np.zeros((self.dim_cvec,self.nz))
            for ii in range(self.dim_cvec):
                self.Vmat_p[ii,:] = np.interp(self.variables['z']["data"],-self.z_eof[::-1],eofs[ii,::-1])
            # self.Vmat_p = readtxt(self.eofs_file, [self.dim_cvec, self.nz])
            #self.Vmat_p = f(self.variables['z']["data"])
            # self.logger.info('ANNAAAA Vmat_p shape: {}'.format(self.Vmat_p.shape))


    def cvt(self, iter: int, state: np.ndarray, v_p: np.ndarray) -> np.ndarray:
        """Forward covariance transformation for parameterized 3D-Var"""
        
        #self.logger.info('cvt state shape: {}'.format(state.shape))
        
        # if True: #iter==1:
        # self.logger.info(f'ANNA   !!!!! iter = {iter}')
        if iter==1:
            # self.totchl=np.zeros(self.nz)
            self.start = self.variables['total_chlorophyll_calculator_result']['start']
            self.stop = self.start + self.variables['total_chlorophyll_calculator_result']['length']
            self.totchl = state[self.start:self.stop]
            # self.totchl = self.variables['total_chlorophyll_calculator_result']["data"]
            
        #if abs(iter)<10:    
        #    self.logger.info('cvt: state = {}'.format(state[:10]))
        #    self.logger.info('cvt: chl = {}'.format(self.totchl))
            
        
        #Vertical operator:
        # self.logger.info('ANNAAAA v_p: {}'.format(v_p.shape))
        Mv = np.matmul(v_p, self.Vmat_p)
        
        #Biogeochemical operator:
        Vv_p=np.zeros([state.size])
        Vv_p[self.start:self.stop] = Mv
        for name in self.pvars:
            start_p = self.variables[name]['start']
            stop_p = start_p + self.variables[name]['length']
            
            MvOverChl=Mv/self.totchl
            Vv_p[start_p:stop_p]=np.where(MvOverChl<-0.99, -0.99, MvOverChl)*state[start_p:stop_p]
        
        return Vv_p

    def cvt_adj(self, iter: int, state: np.ndarray, Vv_p: np.ndarray) -> np.ndarray:
        """Adjoint covariance transformation for parameterized 3D-Var"""
        
        #Biogeochemical operator:
        Mv=np.zeros([self.nz])
        for name in self.pvars:
            start_p = self.variables[name]['start']
            stop_p = start_p + self.variables[name]['length']
            
            Mv+=Vv_p[start_p:stop_p]*state[start_p:stop_p]
            Mv/=self.totchl
            
        # if True: #iter==1:
        #     self.totchl=np.zeros(self.nz)
        #     start = self.variables['total_chlorophyll_calculator_result']['start']
        #     stop = start + self.variables['total_chlorophyll_calculator_result']['length']
        #     self.totchl = state[start:stop]
            
        #if abs(iter)<10:    
        #    self.logger.info('cvt_adj: state = {}'.format(state[:10]))
        #    self.logger.info('cvt_adj: chl = {}'.format(self.totchl))
        
        Mv+=Vv_p[self.start:self.stop]
        
        #Vertical operator:
        v_p=np.matmul(self.Vmat_p, Mv)
        
        return v_p

 

    
    

