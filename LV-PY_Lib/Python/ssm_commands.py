"""
an SSM script is sent to NistPluggableModules' Scripted State Machine (SSM)
as an array of strings. Each string is a single command and the commands are subclassed
with the simplest being a single word such as "stop", then some comma
delimited commands such as "wait,1000", then some commands to control specific modules
with a dot (.) delimited address in the format <Module Type>.<Class Type>.<Instance> where
<instance> is the name of the .ini file used to configure the plugin.

ToDo:  This is a work in progress!  Add child classes for the various Module Types and Plugin Types
"""


class SsmScript:
    """
    Class contains a list of strings with the last string always being the "Stop" command.
    Methods include adding a string to the beginning or to the end of the list (the end
    always being the list element before the "stop" command

    """

    def __init__(self):
        self.cmd_list = ["stop"]

    def prepend(self, cmd):
        """'
        inserts a command string at the beginning of the cmd_list

        """
        # check that the cmd is a string
        if not isinstance(cmd, str):
            raise TypeError("Commands to be inserted must be strings")
        self.cmd_list.insert(0, cmd)

    def append(self, cmd):
        """
        Places a command string just before the "stop" command at the end
        :param cmd:
        :return:
        """
        # check that the cmd is a string
        if not isinstance(cmd, str):
            raise TypeError("Commands to be inserted must be strings")
        i = len(self.cmd_list)-1
        self.cmd_list.insert(i, cmd)


class SsmBaseCmd:
    """
    The base command type is just a simple string
    """
    def __init__(self, cmd):
        if not isinstance(cmd, str):
            raise TypeError("Commands to be inserted must be strings")
        self.cmd = cmd

    def append_to_script(self, script):
        script.append(self.cmd)

    def prepend_to_script(self, script):
        script.prepend(self.cmd)


class SsmModuleCmd(SsmBaseCmd):
    """
    Module Commands have an address <Module Type>.<Class Type>.<Instance>
    """
    def __init__(self, module_type, class_type, instance, cmd):
        for v in locals():
            if not isinstance(cmd, str):
                raise TypeError(f"{v=} tis not a string")
        cmd = cmd + ',#' + module_type + '.' + class_type + "." + instance
        super(SsmModuleCmd, self).__init__(cmd)


class SsmAcPwrSetParameter(SsmModuleCmd):

    def __init__(self, module_type, class_type, instance, cmd='AcPwrSetParameter', AcDc='AC', parameter=None, phase='0', value=None):
        if parameter == None:
            raise ValueError ('Parameter must be a string')
        cmd = cmd + ',' + AcDc + ',' + parameter + ',' + phase + ',' + value
        super(SsmAcPwrSetParameter, self).__init__(module_type, class_type, instance, cmd)


if __name__=='__main__':
    script = SsmScript()
    command = SsmModuleCmd(
       "AcPwr",
       "ChromaAcLoad",
       "SolarArraySim",
       "AcPwrLoopParameter,DC,Power,-1, 10, 0.25,2, 61",)
    command.prepend_to_script(script)
    command = SsmBaseCmd("Wait,1000")
    command.append_to_script(script)
    command = SsmAcPwrSetParameter(
        "AcPwr",
        "ChromaAcLoad",
        "SolarArraySim",
        AcDc = 'DC',
        parameter = 'Voltage',
        value = '10.0'
    )
    command.prepend_to_script(script)
    print(script.cmd_list)

