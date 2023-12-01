import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    Produce Hovmoeller plot of a variable or
    an aggregate variable
    from results of FABM-GOTM 1D
    (adding a line of a constant variable)
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--varname', '-v',
                                type = str,
                                required = False,
                                help = 'Variable to be plotted in the Hovmoeller')

    parser.add_argument(   '--varagg', '-g',
                                type = str,
                                required = False,
                                help = 'Variable to be plotted in the Hovmoeller')

    parser.add_argument(   '--outdir', '-o',
                                type = str,
                                required = True,
                                default = '',
                                help = 'Output Images directory')
    
    parser.add_argument(   '--infile', '-i',
                                type = str,
                                required = True,
                                help = '.nc infile (typically result.nc)')

    parser.add_argument(   '--inref', '-r',
                                type = str,
                                required = True,
                                help = '.nc infile (typically result.nc)')

    parser.add_argument(   '--inobs', '-ob',
                                type = str,
                                required = True,
                                help = '.nc infile (typically result.nc)')

    parser.add_argument(   '--depth', '-d',
                                type = str,
                                required = False,
                                default = '300',
                                help = 'depth limit')

    parser.add_argument(   '--varmin', '-vl',
                                type = str,
                                required = False,
                                default = None,
                                help = 'var limit')

    parser.add_argument(   '--varmax', '-vm',
                                type = str,
                                required = False,
                                default = None,
                                help = 'var limit')

    return parser.parse_args()


args = argument()



# import os,sys
import netCDF4 as NC4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates
# from matplotlib.colors import LogNorm
import datetime
# from datetime import timedelta


#ref = datetime.datetime(2016, 1, 1, 0, 0, 0)

OUTDIR = args.outdir

infile=args.infile
if (not (args.varname is None)) & (not (args.varagg is None)):
    raise ValueError("Both aggregate and normal variable cannot be assigned: choose one")
var = None
aggvar = False
if not (args.varname is None):
    var = args.varname
if not (args.varagg is None):
    var = args.varagg
    aggvar = True

if var is None:
    raise ValueError("Assign one variable (or simple -v or aggragate -g)")

deplim = float(args.depth)

varmin = args.varmin
if not(varmin==None):
   varmin = float(args.varmin)
varmax = args.varmax
if not(varmax==None):
   varmax = float(args.varmax)


fileobs = args.inobs
fileref = args.inref


print(fileobs)
with open(fileobs) as f:
    obs = [line.rstrip().split('\t') for line in f if not line.startswith('#')]
obs_times = pltdates.date2num([datetime.datetime.strptime(o[0], '%Y-%m-%d %H:%M:%S') for o in obs])
obs_values = np.array([o[1] for o in obs], dtype=float)

def readvar(infile,aggvar,var):
    nc = NC4.Dataset(infile)
    AllVars = nc.variables.keys()
    # Read model temperature and coordinates
    time = NC4.num2date(nc['time'], nc['time'].units)
    nT = len(time)
    mpltime = pltdates.date2num(time)
    z = -nc['z'][:, :, 0, 0]
    nZ = z.shape[1]
    if aggvar==False:
        ncvar = nc[var]
        vv = ncvar[:, :, 0, 0]
    else:
        LISTvars = []
        varGroup = var.split('_')[0]
        lenGroup = len(varGroup)
        varElementList = var.split('_')[1:]
        varElement = ('_').join(varElementList)
        lenElement = len(varElement)
        for vname in AllVars:
            if varGroup in vname[:lenGroup]:
                vvElementList = vname.split('_')[1:]
                vvElement = ('_').join(vvElementList)
                if len(vvElement)==lenElement:
                    if varElement in vname[-lenElement:]:
                        print(vname)
                        LISTvars.append(vname)

        if len(LISTvars)<1:
            raise ValueError('Variables for aggregation not found in %s for %s' %(infile,var))
        vv = np.zeros((nT,nZ))
        for vg in LISTvars:
            ncvar = nc[vg]
            vv += ncvar[:,:,0,0]
    nc.close()       
    surfv = vv[:,-1]
    return mpltime,z,vv,surfv
    

print(infile)
mpltime,z,vv,surfv = readvar(infile,aggvar,var)
print(fileref)
print(fileref)
mpltimeref,zref,vv_ref,surfv_ref = readvar(fileref,aggvar,var)

plt.close('all')

# fig, ((ax1, cax1), (ax2, cax2)) = plt.subplots(figsize=(8,6), nrows=2, ncols=2, 
#             gridspec_kw={'width_ratios': [0.95, 0.05]}, sharex='col')
fig, ((ax1, cax1), (ax2, cax2), (ax3, cax3)) = plt.subplots(figsize=(8,8), nrows=3, ncols=2,
                                                            gridspec_kw={'width_ratios': [0.97, 0.03]}, sharex='col')


# Plot modelled and observed sea surface chlorophyll
ax1.plot_date(obs_times, obs_values, '.k', alpha=0.4, label='satellite')
ax1.plot_date(mpltimeref, surfv_ref, '-', label='model, no DA')
ax1.plot_date(mpltime, surfv, '-', label='model, DA (3DVar)')
ax1.set_xlim(mpltime[0], mpltime[-1])
ax1.set_ylabel('chlorophyll [mg $\mathregular{m^{-3}}$]')
ax1.grid()
ax1.legend()
ax1.set_title('surface chlorophyll (a)')
ax1.xaxis.set_major_formatter(
    pltdates.ConciseDateFormatter(ax1.xaxis.get_major_locator()))
# cax1.get_xaxis().set_visible(False)
# cax1.get_yaxis().set_visible(False)
cax1.axis('off')




# Plot modelled variable throughout the water column
mpltime_2d = np.broadcast_to(mpltime[:, np.newaxis], z.shape)
pc = ax2.contourf(mpltime_2d, z, vv_ref, 10, cmap='Greens',extend='max')
cb = fig.colorbar(pc, cax=cax2)
cb.set_label('chlorophyll [mg $\mathregular{m^{-3}}$]')
ax2.set_ylabel('depth [m]')
ax2.set_title('chlorophyll without data assimilation (b)')
ax2.grid()
ax2.xaxis.axis_date()
ax2.set_ylim(deplim, z.min())
ax2.xaxis.set_major_formatter(
    pltdates.ConciseDateFormatter(ax2.xaxis.get_major_locator()))


var_diff = vv-vv_ref
p1 = np.percentile(var_diff,1)
p99 = np.percentile(var_diff,99)
difflim = np.max(np.abs([p1,p99]))
difflim = 0.18
contours = np.linspace(-difflim, difflim, 19)
pc = ax3.contourf(mpltime_2d, z, var_diff, cmap='RdBu_r', levels=contours, extend='both')
cb = fig.colorbar(pc, cax=cax3)
cb.set_label('chlorophyll difference [mg $\mathregular{m^{-3}}$]')
ax3.set_ylabel('depth [m]')
ax3.set_title('impact of data assimilation on chlorophyll (DA (3DVar) - no DA) (c)')
ax3.grid()
ax3.xaxis.axis_date()
ax3.set_ylim(deplim, z.min())
ax3.xaxis.set_major_formatter(
    pltdates.ConciseDateFormatter(ax3.xaxis.get_major_locator()))

fig.tight_layout()


plt.show(block=False)


plt.savefig(f'{OUTDIR}/hovdiff_surf_chl.png',dpi=600)
