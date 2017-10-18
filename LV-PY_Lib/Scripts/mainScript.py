# -*- coding: utf-8 -*-
import time
from lta import Lta
import sys
from lta_err import Lta_Error

class StdTests(object):
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

    #todo: verify decimal numeric errors
    #log features

    #constructor
    def __init__(self,Fs,Fnom,Fsamp,Vnom,Inom,PMUclass,lta,ntries,secwait,ecode):
        try: 
            if PMUclass != "M" and PMUclass != "P":
                raise Exception('Error: Unrecognizable PMU class')

        #Would be good to limit these to safe values            
            self.Fs = int(Fs)
            self.Fnom = float(Fnom)
            self.Fsamp = int(Fsamp)
            self.Vnom = Vnom
            self.Inom = Inom
            self.PMUclass = PMUclass
            self.lta = lta
            self.ntries = ntries
            self.secwait = secwait
            self.ecode = ecode

        except Exception as ex:
            raise ex   

     
    def set_init(self):
        try:
            """ Sets initial default values to the framework"""
            print("Setting default params")
            #Setting Time
            WfrmTime=self.lta.__get__('test.wfrm.time')
            #print WfrmTime
            WfrmTime['WfrmTime']['StartTime'] = float(0.)
            WfrmTime['WfrmTime']['EndTime'] = float(5.)  #test suite especification: 5s

            Error = self.lta.__set__('test.wfrm.time',WfrmTime)
            #print Error
            
            #Setting Config
            WfrmConfig=self.lta.__get__('test.wfrm.config')
            WfrmConfig['WfrmConfig']['T0(UTC)'] = float(0.)
            WfrmConfig['WfrmConfig']['F0'] = float(self.Fnom)
            WfrmConfig['WfrmConfig']['Fs'] = int(self.Fs)  
            WfrmConfig['WfrmConfig']['FSamp'] = int(self.Fsamp)
            Error = self.lta.__set__('test.wfrm.config',WfrmConfig)
            #print WfrmConfig
            
            #Setting Waveform Params
            WfrmParams = self.lta.__get__('test.wfrm.params')    
            #print WfrmParams
            
            #useful indices
            Xm = 0; Fin = 1; Pin = 2; Fh = 3
            VA = 0; VB = 1; VC = 2; IA = 3; IB = 4; IC = 5;
            
            WfrmParams['WfrmParams'][Xm][VA:VC+1] = float(self.Vnom)
            WfrmParams['WfrmParams'][Xm][IA:IC+1] = float(self.Inom)
            WfrmParams['WfrmParams'][Fin][:] = float(self.Fnom)
            WfrmParams['WfrmParams'][Pin][VA] = WfrmParams['WfrmParams'][Pin][IA] = float(0.)
            WfrmParams['WfrmParams'][Pin][VB] = WfrmParams['WfrmParams'][Pin][IB] = float(-120.)
            WfrmParams['WfrmParams'][Pin][VC] = WfrmParams['WfrmParams'][Pin][IC] = float(120.)
            WfrmParams['WfrmParams'][Fh:][:] = float(0.) #all remaining parameters are null
            Error = self.lta.__set__('test.wfrm.params',WfrmParams)
            #print Error
        except Exception as ex:
            raise ex
                 
    def FreqRange(self):
        """Performs the frequency range tests"""
        print ("Performing frequency range tests")
        try:
            self.set_init()
            WfrmParams=self.lta.__get__('test.wfrm.params')
            
            #changing frequencies and running for each value
            ep = 0.01
            freq = self.Fnom - 5.
            fstop = self.Fnom + 5. + ep
            fstep = .1 #test suite specification
            Fin = 1

            while freq<fstop:
                print "freq = ",freq
                WfrmParams['WfrmParams'][Fin][:] = float(freq)
                Error = self.lta.__set__('test.wfrm.params',WfrmParams)
                Error = self.lta.__multirun__(self.ntries,self.secwait,self.ecode)
                freq += fstep
            
        except Exception as ex:
            raise type(ex)("Frequency Range test failure:", freq,"Hz.", ex.message)
            
            
    def Magnitude(self):
        try:
            
            """Performs Voltage and Current Magnitude tests"""
            print ("Performing Magnitude tests")
            self.set_init()
            #useful indices
            Xm = 0; 
            VA = 0; VC = 2; IA = 3; IC = 5;
            
            #Setting Waveform Params
            WfrmParams = self.lta.__get__('test.wfrm.params')    
            
            #changing magnitudes and running for each value
            ep = 0.01
            Vstop = 1.2*self.Vnom + ep
            Istop = 2*self.Inom + ep
            Vstep = .1*self.Vnom 
            Istep = .1*self.Inom
            I = .1*self.Inom
            if self.PMUclass == "M":
                V = 0.1*self.Vnom
            elif self.PMUclass == "P":
                V = 0.8*self.Vnom
            else:
                raise Exception('Error: Unrecognizable PMU class')

            # Voltage and current magnitude tests
            while (V<Vstop):
                print ("Testing " + str(V) + "V; " + str(I) + "A")
                WfrmParams['WfrmParams'][Xm][VA:VC+1] = float(V)
                WfrmParams['WfrmParams'][Xm][IA:IC+1] = float(I)
                Error = self.lta.__set__('test.wfrm.params',WfrmParams)
#                print Error
                Error = self.lta.__multirun__(self.ntries,self.secwait,self.ecode)
#                print Error
                V += Vstep
                I += Istep
            
            # sets default voltage for remaining current tests            
            WfrmParams['WfrmParams'][Xm][VA:VC+1] = float(self.Vnom)
            Error = lta.__set__('test.wfrm.params',WfrmParams)
            
            # Remaining Current magnitude tests
            while (I<Istop):
                print ("Testing " + str(Vnom) + "V; " + str(I) + "A")
                WfrmParams['WfrmParams'][Xm][IA:IC+1] = float(I)
                Error = lta.__set__('test.wfrm.params',WfrmParams)
#                print Error
                Error = self.lta.__multirun__(self.ntries,self.secwait,self.ecode)
#                print Error
                I += Istep
                
#            assert 'true' == 'false', 'This is an intentional error forced by the Magnitude test\n\n'                 
                
        except Exception as ex:
            raise type(ex)("Magnitude test failure:" + str(V) + "V,"+ str(I) +"A." + ex.message)
       
    def Harm(self):
        try:
            
            """Performs the harmonics tests"""
            print ("Performing harmonic tests")
            self.set_init()
            
            fmax = 50*self.Fnom
            #verify Nyquist criteria
            if (self.Fsamp)<(2*fmax):
                raise Exception ("Warning: the chosen Fsamp = " + str(self.Fsamp) + 
                "Hz is not within the Nyquist criteria for the highest frequency = " + str(fmax))            
            
            #changing harmonics and running for each value
            if self.PMUclass == "M":
                Khm = 0.1
            elif self.PMUclass == "P":
                Khm = 0.01
            else:
                raise Exception('Error: Unrecognizable PMU class')

            #useful indices
            Kh = 5; Fh = 3
            
            WfrmParams = self.lta.__get__('test.wfrm.params') 
            WfrmParams['WfrmParams'][Kh][:] = float(Khm)

            
            for i in range(2,51):
                print ("Testing for harmonic frequency " + str(self.Fnom*i) + "Hz")
                WfrmParams['WfrmParams'][Fh][:] = float(self.Fnom*i)
                Error = lta.__set__('test.wfrm.params',WfrmParams)
                print "Trying to run..."
                Error = lta.__multirun__(self.ntries,self.secwait,self.ecode)

#            assert 'true' == 'false', 'This is an intentional error forced by the Harmonic test\n\n'    

        except Exception as ex:
            raise type(ex)("Harmonic test failure:", i ," harmonic.", ex.message)

    def OutOfBand(self):
        try:
            """Performs the out-of-band interference tests"""
            print ("Performing out of band interference tests")
            self.set_init()

            fnom = [self.Fnom, self.Fnom + Fs/2, self.Fnom - Fs/2]

            for f0 in fnom:
                fmax = 2*f0; print(" --- Out-of-band test for f0 = " + str(f0))
                #verify Nyquist criteria
                if (self.Fsamp)<(2*fmax):
                    raise Exception ("Warning: the chosen Fsamp = " + str(self.Fsamp) + 
                    "Hz is not within the Nyquist criteria for the highest frequency = " + str(fmax))
    
                #useful indices
                Fh = 3; Kh = 5
    
                WfrmParams = self.lta.__get__('test.wfrm.params')
                #10% nominal magnitude
                WfrmParams['WfrmParams'][Kh][:] = float(.1)             
                
                #changing interfering frequencies and running for each value            
                i = 0
                fi = f0 - self.Fs/2
                print("Frequency: " + str(fi) + "Hz")
                while fi != 10:
                    fi = max(f0 - self.Fs/2 - (.1*2**i),10)
                    print("Frequency: " + str(fi) + "Hz")
                    WfrmParams['WfrmParams'][Fh][:] = float(fi)
                    Error = lta.__set__('test.wfrm.params',WfrmParams)
                    i += 1
                    Error = lta.__multirun__(self.ntries,self.secwait,self.ecode)
            
                i = 0
                while fi != fmax:
                    fi = min(f0 + self.Fs/2 + (.1*2**i),fmax)
                    print("Frequency: " + str(fi) + "Hz")
                    WfrmParams['WfrmParams'][Fh][:] = float(fi)
                    Error = lta.__set__('test.wfrm.params',WfrmParams)
                    i += 1
                    Error = lta.__multirun__(self.ntries,self.secwait,self.ecode)
        except Exception as ex:
            raise type(ex)("Out of band test failure:", f0,"Hz." , ex.message)
        
    def MeasBand(self):
        try:
            """Performs the Measurement Bandwidth tests"""
            print ("Performing measurement bandwitdth tests")
            self.set_init()
            
            #range of modulation frequency: 0.1:Fmax
            if self.PMUclass == "M":
                Fmax = 5.
                if self.Fs/5 < 5:
                    Fmax = self.Fs/5
            elif self.PMUclass == "P":
                Fmax = 2.
                if self.Fs/10 < 2:
                    Fmax = self.Fs/10
            else:
                raise Exception('Error: Unrecognizable PMU class')
                
            #useful indices
            Fa = 6; Ka = 7; Fx = 8; Kx = 9
               
            WfrmTime = lta.__get__('test.wfrm.time')
            WfrmParams = lta.__get__('test.wfrm.params')
            
            #Amplitude Modulation
            WfrmParams['WfrmParams'][Kx][:] = 0.1
            WfrmParams['WfrmParams'][Ka][:] = 0.
            fmod = range(1,int(Fmax*10),2) + [int(Fmax*10)]
            for f in fmod:
                print float(f)/10
                WfrmParams['WfrmParams'][Fx][:] = float(f)/10
                Tcycle = (10./f)
                if Tcycle*2. > 5.:
                   WfrmTime['WfrmTime']['EndTime'] = Tcycle*2.
#                   print Tcycle*2.
                else:
                   WfrmTime['WfrmTime']['EndTime'] = 5. 
                Error = lta.__set__('test.wfrm.time',WfrmTime)
                #print Error
                Error = lta.__set__('test.wfrm.params',WfrmParams)
                #print Error
                Error = lta.__multirun__(self.ntries,self.secwait,self.ecode)
                #print Error
            WfrmParams['WfrmParams'][Fx][:] = 0.
                
            #Phase Modulation
            WfrmParams['WfrmParams'][Kx][:] = 0.
            WfrmParams['WfrmParams'][Ka][:] = 0.1
            for f in fmod:
                print float(f)/10
                WfrmParams['WfrmParams'][Fa][:] = float(f)/10
                Tcycle = (10./f)
                if Tcycle*2. > 5.:
                   WfrmTime['WfrmTime']['EndTime'] = Tcycle*2.
                   print Tcycle*2.
                else:
                   WfrmTime['WfrmTime']['EndTime'] = 5. 
                Error = lta.__set__('test.wfrm.time',WfrmTime)
                #print Error
                Error = lta.__set__('test.wfrm.params',WfrmParams)
                #print Error
                Error = lta.__multirun__(self.ntries,self.secwait,self.ecode)
                #print Error
            WfrmParams['WfrmParams'][Fa][:] = 0.
            
        except Exception as ex:
            raise type(ex)("Measurement Bandwidth test failure: Kx=", Kx,", Ka=", Ka,", fmod=", f,"Hz.", ex.message)
        
    def RampFreq(self):
        try:
            """Performs the ramp of system frequency tests - positive and negative in sequence"""
            print("Performs the ramp of system frequency tests - positive and negative in sequence")
            self.set_init()            
            Error = WfrmTime = lta.__get__('test.wfrm.time')
            Error = WfrmParams = lta.__get__('test.wfrm.params')
            
            #ramp ranges
            if int(self.Fs) == 12:            
                mfreq = (2. + 1./3)
            else:
                mfreq = min(self.Fs/5,5.)
            
            print("mfreq = ", str(mfreq))
            
            freqs = {"P":(self.Fnom-2.,self.Fnom+2.), "M":(self.Fnom-mfreq,self.Fnom+mfreq)}
            
            print(freqs)

            StartFreq = freqs[self.PMUclass][0]
            StopFreq = freqs[self.PMUclass][1]

            WfrmTime['WfrmTime']['StartTime'] = - (StopFreq - StartFreq)  #for 1Hz/s             
            WfrmTime['WfrmTime']['EndTime'] = (StopFreq - StartFreq)  #for 1Hz/s 
            Error = lta.__set__('test.wfrm.time',WfrmTime)
            print("Start Freq = " + str(StartFreq) + "; Stop Freq = " + str(StopFreq) + "\n")

            #useful indices
            Rf = 10; Fin = 1

            WfrmParams['WfrmParams'][Fin][:] = float(StartFreq)
            print("Positive ramp frequency")
            WfrmParams['WfrmParams'][Rf][:] = 1.
            Error = lta.__set__('test.wfrm.params',WfrmParams)
            Error = lta.__multirun__(self.ntries,self.secwait,self.ecode)
            
            print("Negative ramp frequency")
            WfrmParams['WfrmParams'][Fin][:] = float(StopFreq)
            WfrmParams['WfrmParams'][Rf][:] = -1.
            Error = lta.__set__('test.wfrm.params',WfrmParams)
            Error = lta.__multirun__(self.ntries,self.secwait,self.ecode)
            
        except Exception as ex:
            raise type(ex)("Ramp of frequency test failure: ", "Start Freq = ", str(StartFreq), "; Stop Freq = ", str(StopFreq), ".", ex.message)
            
    def StepChanges(self):
        try:
            """Performs the step changes tests"""
            print("Performs the step changes tests")
            self.set_init()

            #useful indices
            KaS = 11; KxS = 12
            WfrmTime = lta.__get__('test.wfrm.time')
            WfrmParams = lta.__get__('test.wfrm.params')
            
            StartTime = float(WfrmTime['WfrmTime']['StartTime'])            
            EndTime = float(WfrmTime['WfrmTime']['EndTime'])
            
            ns = range(10)            
            mag_steps = [0.1, -0.1, 0., 0.]
            phase_steps = [0., 0., 10, 10]
            ntests = range(4)            
            
            # steps in magnitude and phase
            for t in ntests:
                for n in ns: 
                    WfrmParams['WfrmParams'][KxS][:] = mag_steps[t]
                    WfrmParams['WfrmParams'][KaS][:] = phase_steps[t]
                    WfrmTime['WfrmTime']['StartTime'] = StartTime + float(n/(10*self.Fs))-2.5
                    WfrmTime['WfrmTime']['EndTime'] = EndTime + float(n/(10*self.Fs))-2.5
                    Error = lta.__set__('test.wfrm.time',WfrmTime)
                    Error = lta.__set__('test.wfrm.params',WfrmParams)
                    Error = lta.__multirun__(self.ntries,self.secwait,self.ecode)

        except Exception as ex:
            raise type(ex)("Step change test failure: ", "MagStep = ", mag_steps[t], "; PhaseStep = ", phase_steps[t], ".", ex.message) 

    def RepLatency(self):
        try:
            """Performs the reporting latency tests"""
            print("Performs the reporting latency tests")        
            self.set_init()
            Error = lta.__multirun__(self.ntries,self.secwait,self.ecode)
        except Exception as ex:
            raise type(ex)("Reporting latency test failure.", ex.message)  
            
    def SetFs(self,Fs):
        try:
            self.Fs = Fs
        except Exception as ex:
            raise ex

            
# ------------------ MAIN SCRIPT ---------------------------------------------
#------------------- following code must be in all scripts--------------------
lta = Lta("127.0.0.1",60100)    # all scripts must create  an Lta object

try:
    lta.connect()                   # connect to the Labview Host
#---------------------Script code goes here------------------------------------

    print lta

    UsrTimeout = lta.s.gettimeout()

    Fnom = 63
    Fs_ini = 60.  #doesnt matter this default value, to be changed later
    Fs_list = {60:[10,12,15,20,30,60],50:[10,25,50], 63:[10]} #63 inserted for testing
    FSamp = 9600.
    Vnom = 70.
    Inom = 5.
    PMUclass = "M"
    
    #list of exceptions             
    ex_list = []

    ntries = 5  #number of tries for each run
    secwait = 5 #seconds to wait before trying again
    ecode = {5605}  #set of error codes under which we need to try again

    #How to call StdTests:
    #MyTest = StdTests(Fs,Fnom,Fsample,Vnom,Inom,PMUclass,lta)
    t = StdTests(Fs_ini,Fnom,FSamp,Vnom,Inom,PMUclass,lta,ntries,secwait,ecode)
    #list of tests to be performed
    func_list = [t.Magnitude, 
                 #t.Harm, 
                 #t.FreqRange, 
                 #t.OutOfBand,
                 #t.MeasBand, 
                 #t.RampFreq, 
                 #t.StepChanges, 
                 #t.RepLatency
                 ]     

    #execution of tests for each Fs
    for Fs in Fs_list[Fnom]:
        t.SetFs(Fs); print("\n\n ---- Test for Fs = " + str(Fs))
        for my_func in func_list:
            try:
                lta.s.settimeout(60)   
                my_func()
                lta.s.settimeout(UsrTimeout)
            except Exception as ex:
                print "Exception going to LV in the end:"
                print ex
                ex_list.append(ex)
    
    print "FINAL ERROR LIST::"
    print ex_list
    
    for ex in ex_list:
        err = Lta_Error(ex,sys.exc_info())  #format a labview error
        lta.send_error(err,3,'log')       #send the error to labview for log

#------------------all scripts should send their errors to labview------------
except Exception as ex:
    err = Lta_Error(ex,sys.exc_info())  #format a labview error
    lta.send_error(err,3,'Abort')       #send the error to labview for display
    lta.close()
    print err
