"""
Module_class.py provides properties and methods
for manipulating NIST Pluggable Modules.
"""


class Module:
    """
    The Module class defines a standard set of NISTPluggableModule (NPM) properties
    and methods for getting module instance configurations and measurements
    and for setting configurations
    """

    def __init__(self,
                 module_type=None,  # The type of the NPM
                 class_type=None,
                 instance=None
                 ):
        if (module_type is None) or (class_type is None) or (instance is None):
            raise ValueError(" parameters must be as follows:"
                             " module_type must be the name of a valid NISTPluggable Module type,"
                             " class_type must be a valid plugin type for the module_type,"
                             " instance must be the file name of the loaded .ini configuration file.")
        else:
            self.module_type = module_type
            self.class_type = class_type
            self.instance = instance
            self.instance_name = self.module_type+'.'+self.class_type+'.'+self.instance

            self.config = None
            self.meas = None

    def get_config(self,lta):
        self.config = lta.__get__(self.instance_name+',Config')



