"""
Test for the module_class
"""

from module_class import NPModuleAcPwr
from lta import Lta


# ------------------- following code must be in all scripts--------------------
lta = Lta("127.0.0.1", 60100)  # all scripts must create  an Lta object
lta.connect()  # connect to the Labview Host

module = NPModuleAcPwr('AcPwr', 'NHRDCPower', 'SolarArraySim', lta)
#module.get_config()
#print(module.config)
#module.set_config()
module.get_meas()



