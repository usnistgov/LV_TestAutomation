# -*- coding: utf-8 -*-
import time
from lta import Lta
import sys
from lta_err import Lta_Error

#------------------- following code must be in all scripts--------------------
lta = Lta("127.0.0.1",60100)    # all scripts must create  an Lta object

try:
    lta.connect()                   # connect to the Labview Host
#---------------------Script code goes here------------------------------------
    from PmuTests import pmuTests
    UsrTimeout = lta.s.gettimeout()
    
    # list of exceptions
    ex_list= []
    
    # Set up the test parameters here    
    Fnom = 50
    Frange = 0.1
    Vnom = 70
    Inom = 5
    
    # Set up the parameters for multiple test runs
    ntries = 30 # max number of tries allowed
    secwait = 10 # seconds to wait before trying again
    ecode = {5605} # set of error codes under with we need to try again
    
    # Don't run the tests if the Sync Module is not Locked
    LockStatus = lta.__get__('Sync.LockStatus')
    if LockStatus[None]==False:
        raise Exception('Sync Module is Not Locked')
        
     # set up the pmuTests
    t = pmuTests(lta,Fnom,Frange,Vnom,Inom,ntries,secwait,ecode)
    t.set_default()
    
    func_list = [t.FreqRange]
    
    
    for my_func in func_list:
        try:
            lta.s.settimeout(60)
            my_func()
            lta.s.settimeout(UsrTimeout)
        except Exception as ex:
            print "Exception going to LV in the end:"
            print ex
            ex_list.append(ex)
            err = Lta_Error(ex,sys.exc_info())
            lta.send_error(err,3,'log')
        
    print "FINAL ERROR LIST::"
    print ex_list
    
    lta.close()
    

#------------------all scripts should send their errors to labview------------
except Exception as ex:
    err = Lta_Error(ex,sys.exc_info())  #format a labview error
    lta.send_error(err,3,'Abort')       #send the error to labview for display
    lta.close()
    print err
