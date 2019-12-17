# -*- coding: utf-8 -*-
from lta import Lta
import sys
from lta_err import Lta_Error

#------------------- following code must be in all scripts--------------------
lta = Lta("127.0.0.1",60100)    # all scripts must create  an Lta object
try:
    lta.connect()                   # connect to the Labview Host
#---------------------Script code goes here------------------------------------
    
    variables = ['A','B','C']
    for x in variables:   
        CommsData = lta.__get__(x)    
        CommsData['D']=CommsData['D']+1
        lta.__set__(x,CommsData)
        error = lta.__run__()
        CommsData = lta.__get__('D')
        print CommsData['D']
        
    CommsData = lta.__get__('Enum')  
    enum = CommsData['MyCluster']['Enum In']
    val = enum(enum.Val)
    print(val)
    lta.__set__('Enum',CommsData)
   
#------------------all scripts should send their errors to labview------------
except Exception as ex:
    err = Lta_Error(ex,sys.exc_info())  #format a labview error
    lta.send_error(err,3,'Abort')       #send the error to labview for display
    lta.close()
    print err
