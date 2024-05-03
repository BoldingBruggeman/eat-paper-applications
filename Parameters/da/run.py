import eatpy
#import cvt
#import keep
#import plug_propagate
import control_DA
experiment = eatpy.models.GOTM(
#diagnostics_in_state=["total_chlorophyll_calculator_result"]
fabm_parameters_in_state=["instances/P1/parameters/sum"]
)
#experiment.add_plugin(cvt.Cvt())
experiment.add_plugin(control_DA.MyPlugin())
#experiment.add_plugin(plug_propagate.PropagateChlTot())
filter = eatpy.PDAF(eatpy.pdaf.FilterType.ESTKF)
#experiment.add_observations("total_chlorophyll_calculator_result", "Exp_OC_HT_P_HE_FC.dat")
#experiment.add_observations("total_chlorophyll_calculator_result", "Exp_OC_HT_P_LE_FC.dat")
experiment.add_observations("P1_Chl[-1]", "../observations/P1_Chl_cci_5d.dat")
#experiment.add_observations("total_chlorophyll_calculator_result", "Exp_OC_HT.dat")
experiment.run(filter)
