"""
Test for the module_class
"""

from module_class import Module
from lta import Lta


# ------------------- following code must be in all scripts--------------------
lta = Lta("127.0.0.1", 60100)  # all scripts must create  an Lta object
lta.connect()  # connect to the Labview Host

#module = Module('Sync', 'PXI_MultiTrig', 'Dyn3_PMUCal')
#module.get('ClockProperties',lta)

module = Module('FGen', 'NiPxi6733', 'PMU (SteadyState)')
print(module.instance_name)
module.get('FunctionParams',lta)
print(module.config)
module.get('FunctionArbs',lta)
print(module.config)
module.get('FunctionSampleRate',lta)
print(module.config)



