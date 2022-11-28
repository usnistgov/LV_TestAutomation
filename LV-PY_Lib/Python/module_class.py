"""
Module_class.py provides properties and methods
for manipulating NIST Pluggable Modules.
"""
from lta import Lta
from lta_err import LV_to_Py_Error


class NPModule:
    """
    The NPModule class defines a standard set of NISTPluggableModule (NPM) properties
    and methods for getting module instance configurations and measurements
    and for setting configurations


    """

    def __init__(self,
                 module_type=None,  # The type of the NPM
                 class_type=None,
                 instance=None,
                 lta=None
                 ):
        if not isinstance(lta, Lta):
            raise ValueError("Module class requires a valid, connected Lta instance as the last parameter")
        if (module_type is None) or (class_type is None) or (instance is None):
            raise ValueError(" parameters must be as follows:"
                             " module_type must be the name of a valid NISTPluggable Module type,"
                             " class_type must be a valid plugin type for the module_type,"
                             " instance must be the file name of the loaded .ini configuration file.")
        else:
            self.module_type = module_type
            self.class_type = class_type
            self.instance = instance
            self.instance_name = self.module_type + '.' + self.class_type + '.' + self.instance
            self.lta = lta

    def __get__(self, arg):
        return self.lta.__get__(self.instance_name + arg)

    def __set__(self, arg, value):
        error = self.lta.__set__(self.instance_name + arg, value)
        if error['error out']['status']:
            raise LV_to_Py_Error


class NPModuleAcPwr(NPModule):
    def __init__(self,
                 module_type='AcPwr',  # The type of the NPM
                 class_type=None,
                 instance=None,
                 lta=None
                 ):
        super().__init__(module_type, class_type, instance, lta)
        self.config = None
        self.meas = None

    def get_config(self):
        self.config = self.__get__(',Config')

    def set_config(self):
        self.__set__(',Config', self.config)

    def get_meas(self):
        self.meas = self.__get__(',Meas')


class NPModuleFGen(NPModule):

    def __init__(self,
                 module_type='FGen',
                 class_type=None,
                 instance='',
                 lta=None
                 ):
        super().__init__(module_type, class_type, instance, lta)
        self.params = None
        self.arbs = None
        self.samplerate = None

    def get_params(self):
        self.params = self.__get__(',FunctionParams')

    def set_params(self):
        self.__set__(',FunctionParams', self.params)

    def get_arbs(self):
        self.arbs = self.__get__(',FunctionArbs')

    def set_arbs(self):
        self.__set__(',FunctionArbs', self.arbs)

    def get_samplerate(self):
        self.samplerate = self.__get__(',FunctionSampleRate')

    def set_samplerate(self):
        self.__set__(',FunctionSampleRate', self.samplerate)


class NPModuleAnalysis(NPModule):

    def __init__(self,
                 module_type='Analysis',
                 class_type=None,
                 instance=None,
                 lta=None
                 ):
        super().__init__(module_type, class_type, instance, lta)
        self.state = None
        self.config = None
        self.duration = None
        self.params = None

    def get_state(self):
        self.state = self.__get__(',State')

    def get_config(self):
        self.config = self.__get__(',Config')

    def set_config(self):
        self.__set__(',Config', self.config)

    def get_duration(self):
        self.duration = self.__get__(',Duration')

    def set_duration(self):
        self.__set__(',Duration', self.duration)

    def get_params(self):
        self.params = self.__get__(',FunctionParams')

    def set_params(self):
        self.__set__(',FunctionParams', self.params)


class NPModuleSync(NPModule):

    def __init__(self,
                 module_type='Sync',
                 class_type=None,
                 instance='',
                 lta=None
                 ):
        super().__init__(module_type, class_type, instance, lta)
        self.triggertime = None
        self.lockstatus = None
        self.clockproperties = None

    # Not yet implemented in Labview
    # def get_triggertime(self):
    #     self.triggertime = self.__get__(',TriggerTime')
    #
    # def get_lockstatus(self):
    #     self.lockstatus = self.__get__(',LockStatus')

    def get_clockproperties(self):
        self.clockproperties = self.__get__(',ClockProperties')

    def set_clockproperties(self):
        self.__set__(',ClockProperties', self.clockproperties)

    def set_timedtrigger(self, arg):
        self.__set__(',TimedTrigger', arg)

    def set_softwaretrigger(self):
        self.__set__('SoftwareTrigger', None)


class NPModuleSensor(NPModule):

    def __init__(self,
                 module_type='Sensor',  # The type of the NPM
                 class_type=None,
                 instance=None,
                 lta=None
                 ):
        super().__init__(module_type, class_type, instance, lta)
        self.config = None
        self.meas = None

    def get_config(self):
        self.config = self.__get__(',Config')

    def set_config(self):
        self.__set__(',Config', self.config)

    def get_meas(self):
        self.meas = self.__get__(',Meas')
