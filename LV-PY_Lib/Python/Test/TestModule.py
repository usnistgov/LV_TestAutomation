"""
Test for the module_class
"""

import module_class as M
from lta import Lta
from lta_err import Lta_Error
import sys

class Tests(object):

    def __init__(self):
        try:
            self.lta = Lta("127.0.0.1", 60100)  # all scripts must create  an Lta object
            self.lta.connect()  # connect to the Labview Host
        except Exception as ex:
            err = Lta_Error(ex,sys.exc_info())  #format a labview error
            self.lta.send_error(err,3,'Abort')       #send the error to labview for display
            self.lta.close()
            print (err)


    def test_acpwr(self):
        print('testing ACPwr.NHRDCPwr.SolarArraySim')
        module = M.NPModuleAcPwr(class_type='NHRDCPower', instance='SolarArraySim', lta=self.lta)
        module.get_config()
        print(module.config)
        module.set_config()
        #module.get_meas()
        #print(module.meas)

    def test_fgen(self):
        print ('testing FGen.NiPxi6733')
        module = M.NPModuleFGen(class_type='NiPxi6733', instance='PMU (SteadyState)', lta=self.lta)
        module.get_params()
        print(module.params)
        module.set_params()
        module.get_arbs()
        print(module.arbs)
        module.set_arbs()
        module.get_samplerate()
        print(module.samplerate)
        module.set_samplerate()

    def test_analysis(self):
        print ('testing Analysis.PmuAnalysis.Pmu (SteadyState)')
        module = M.NPModuleAnalysis(class_type='PmuAnalysis', instance='Pmu (SteadyState)',lta=self.lta)
        module.get_params()
        print(module.params)
        module.set_params()
        module.get_config()
        print(module.config)
        module.set_config()
        module.get_duration()
        print(module.duration)
        module.set_duration()
        module.get_state()
        print(module.state)


    def test_sync(self):
        print ('testing Sync.PXI_MultiTrig')
        module = M.NPModuleSync(class_type='PXI_MultiTrig',instance='Dyn3_PMUCal', lta=self.lta)
        module.get_clockproperties()
        print(module.clockproperties)
        module.set_clockproperties()
        

    # this will require some modifications to labview Test.lvclass:GetModuleIndex.vi
    def test_fgen_all_instances(self):
        print ('testing access to all instances of FGen module')
        print ('testing FGen.NiPxi6733')
        module = M.NPModuleFGen(class_type='NiPxi6733', instance='', lta=self.lta)
        module.get_params()
        print(module.params)
        module.set_params()
        module.get_arbs()
        print(module.arbs)
        module.set_arbs()
        module.get_samplerate()
        print(module.samplerate)
        module.set_samplerate()        










#============================================= Main Program ============================================================
t = Tests()

test_list = [
             #t.test_acpwr,     # testing ACPwr.NHRDCPwr.SolarArraySim
             t.test_fgen,       # testing Analysis.PmuAnalysis.Pmu (SteadyState)
             t.test_analysis,   # testing Analysis.PmuAnalysis.Pmu (SteadyState)
             t.test_sync,        # testing Sync.PXI_MultiTrig
             #t.test_fgen_all_instances  # see note in the function def above
            ]

for test in test_list:
    test()





#module.get_config()
#print(module.config)
#module.set_config()
#module.get_meas()
#print(module.meas)

t.lta.close()

