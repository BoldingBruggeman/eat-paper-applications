

SETUP=BFMvar # assimilation run
INDIR=$PWD/../$SETUP/
INFILE=$INDIR/result_0001.nc
REF=Free # free run
INREF=$PWD/../$REF/
REFFILE=$INREF/result.nc
OBSFILE=$INDIR/ToAssimilate/nrt_chlsat.obs

OUTBASE=$PWD/FIGURES/ # outdir for figures
OUTDIR=$OUTBASE/$SETUP/
mkdir -p $OUTDIR

DEPTH=200
AGGVAR=P_run # net primary production
python plot_hovmoeller_diffref.py -i $INFILE -o $OUTDIR -g $AGGVAR -d $DEPTH -r $REFFILE -ob $OBSFILE 

DEPTH=300
AGGVAR=P_Chl # chlorophyll
python plot_hovmoeller_diffref_chl.py -i $INFILE -o $OUTDIR -g $AGGVAR -d $DEPTH -r $REFFILE -ob $OBSFILE -vl 0.0 -vm 0.5

