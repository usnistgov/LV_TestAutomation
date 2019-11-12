# -*- coding: utf-8 -*-
from lta import Lta



class pmuTests(object):
    """This object is intended to be a set of standard tests that shall follow the test suit specification, 
    whose methods are capable of setting parameters and sending messages to actually run them through a 
    Labview framework
    
    Attributes:    
    Fs 
    Fnom 
    Fsample
    Vnom 
    Inom 
    PMUclass 
    lta   - object to connect Labview host
    ntries - Number of running tries
    secwait - Seconds to wait before next try
    ecode - error code for trying again
    """


    def __init__(self,lta,Fnom,Frange,Vnom,Inom,ntries,secwait,ecode):
        try:
            self.lta = lta
            self.Fnom = float(Fnom)
            self.Frange = float(Frange)
            self.Vnom = float(Vnom)
            self.Inom = float(Inom)
            self.ntries = ntries
            self.secwait = secwait
            self.ecode = ecode
            
            # indices into the Function Prameter Array
            self.Indices = {
                "Xm": 0,
                "VA": 0,
                "VB": 1,
                "VC": 2,
                "IA": 3,
                "IB": 4,
                "IC": 5,
                "Fin": 1,
                "Pin": 2,
                "Fh": 3
                }
            
        except Exception as ex:
            raise ex
            
    # Sets the default waveform parameters for each test
    def set_default(self):
        print("Setting Default FGen Parameters")
        
        # indices into the Function Prameter Array        
        Xm = self.Indices['Xm']
        VA = self.Indices['VA']
        VC = self.Indices['VC']
        IA = self.Indices['IA']
        IC = self.Indices['IC']
        Fin = self.Indices['Fin']
        
        
        try:
            WfrmParams = self.lta.__get__("FGen.FunctionParams")
            Params = WfrmParams[None]
            Params[Xm][VA:VC+1] = float(self.Vnom)
            Params[Xm][IA:IC+1] = float(self.Inom)
            Params[Fin][:] = float(self.Fnom)
            WfrmParams[None] = Params
            Error = self.lta.__set__("FGen.FunctionParams",WfrmParams)
        except Exception as ex:
            raise ex
            
            
    # Frequency Range Tests        
    def FreqRange(self):
        print ("Performing steady state frequency range tests")
        
        freq = self.Fnom - self.Frange
        fstop = self.Fnom + self.Frange + 0.01
        fstep = 0.1
        
        # indices into the signal parameters
        Fin = self.Indices['Fin']
        
        try:
            WfrmParams = self.lta.__get__("FGen.FunctionParams")
        except Exception as ex:
            raise ex
           
        Params = WfrmParams[None]
        
        while freq<fstop:
            print "freq = ", freq
            Params[Fin][:] = float(freq)
            WfrmParams[None] = Params
            
            try:
                Error = self.lta.__set__("FGen.FunctionParams",WfrmParams)
                Error = self.lta.__multirun__(self.ntries,self.secwait,self.ecode)
            except Exception as ex:
                raise type(ex)("Frequency Range test failure:"+ex.message)
                
            freq += fstep
            
            
        
    
        
        