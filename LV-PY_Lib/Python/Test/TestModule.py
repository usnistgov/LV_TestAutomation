"""
Test for the module_class
"""

from module_class import Module
from lta import Lta

module = Module('AcPwr', 'ChromaAcLoad', 'SolarArraySim')
print(module.instance_name)

# ------------------- following code must be in all scripts--------------------
lta = Lta("127.0.0.1", 60100)  # all scripts must create  an Lta object
lta.connect()  # connect to the Labview Host

module.get_config(lta)
print(module.config)