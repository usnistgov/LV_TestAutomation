from ssm_commands import SsmScript
from ssm_commands import SsmBaseCmd
from lta import Lta

script = SsmScript()
command = SsmBaseCmd('Wait,1000')
command.prepend_to_script(script)

# ------------------- connect to Lta--------------------
lta = Lta("127.0.0.1", 60100)  # all scripts must create  an Lta object
lta.connect()  # connect to the Labview Host

lta.__send_script__(script)