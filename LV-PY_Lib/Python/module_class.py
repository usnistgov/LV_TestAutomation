"""
Module_class.py provides properties and methods
for manipulating NIST Pluggable Modules.
"""
from lta import Lta
from lta_err import Lta_Error
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
        if not isinstance(lta,Lta):
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


class NPModuleAcPwr(NPModule):
    def __init__(self,
                 module_type=None,  # The type of the NPM
                 class_type=None,
                 instance=None,
                 lta = None
                 ):
        super().__init__(module_type, class_type, instance, lta)
        self.config = None
        self.meas = None

    def get_config(self):
        self.config = self.lta.__get__(self.instance_name + ',Config')
        #print(self.config)

    def set_config(self):
        error = self.lta.__set__(self.instance_name + ',Config', self.config)
        if error['error out']['status']:
            raise LV_to_Py_Error

    def get_meas(self):
        self.meas = self.lta.__get__(self.instance_name + ',Meas')
        #print(self.meas)