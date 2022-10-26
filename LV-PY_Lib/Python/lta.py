# -*- coding: utf-8 -*-
""" LabVIEW Test Automation """
# class lta: Labview Test Automation
from collections import OrderedDict
from lta_parse import Lta_Parse
from lta_unparse import Lta_Unparse
from lta_err import Lta_Error
from lta_err import LV_to_Py_Error
import socket
import packet
import sys
import time
 
class Lta_Command:
    """ This object is a wrapper dictionary that wraps an Lta "dataStruct" 
    dictionary in a command dictionary ready to be unparsed and sent to LabVIEW

    useage:
    cmdDict = Lta_Command(command, dataStruct)     
    command is the command message string recognized by your LabVIEW Host.
            
    dataStruct is an OrderedDictionary that conforms to the structure that
    LabVIEW is expecting for arriving data.
            
    Note that LabVIEW violates the spirit of XML by requiring tags to be in 
    Order expected by the typedef of the object that is being unflattened.
    That is why we need to use OrderedDictionaries
    """
        
    def __init__(self,command=None,arg=None):
        self.command = command
        self.arg = arg
        if not isinstance(arg,str):
            self.arg = Lta_Unparse(self.arg)
        self.cmdDict = {'CommsData': OrderedDict([('Command',self.command),('XMLData', self.arg)])}
       
    def __str__(self):
        return str(self.cmdDict)
        
    def __len__(self):
        return self.cmdDict.__len__()    
   
          
class Lta():
    """Labview Test Automation class"""
    def __init__(self,host=None,port=None):
        self.host = host
        self.port = port
        self.s = ''
        return

    def connect(self): 
            self.s=socket.create_connection((self.host,self.port))
            self.s.settimeout(0.2)
            
    def close(self):
        try:
            self.s.close()
        except IOError as e:
            print(e)
        
    def send_error(self,err,pri,sev):
        errDict = Lta_Command('ClientError',err.LvError(pri,sev))
        errXML = Lta_Unparse(errDict.cmdDict)
        packet.SendPacket(self.s,errXML)    

    def __get__(self,arg):
        """ for now, arg is the XML string of the get command """
        try:
            UsrTimeout = self.s.gettimeout()            
            self.s.settimeout(1)
            cmd = Lta_Command('get', arg)
            self.s.settimeout(UsrTimeout)
            xml = Lta_Unparse(cmd.cmdDict)
            packet.SendPacket(self.s,xml)
            Completed = False
            n = 0; nmax = 50
            #loop needed to receive all packages from LV
            while (not Completed) and n<=nmax:
                CommsData = packet.ReceivePacket(self.s)
                CommsData = Lta_Parse(CommsData)
                if CommsData['CommsData']['Command'] == 'Get':
                    Data = Lta_Parse(CommsData['CommsData']['XMLData'])
                else:
                    Completed = CommsData['CommsData']['Command']=='LtaGetComplete'
                    Error = Lta_Parse(CommsData['CommsData']['XMLData'])
                n += 1
           
            if n>nmax:
                print( "Get was not acknowledged as completed")
            if n>2 or Error['error out']['status']:
                raise LV_to_Py_Error(Error)
            else:
                return Data

        except (IOError, Exception) as e:
            #clear the messages before raising e
            # print( "Got exception, clearing get command messages")
            #if not Completed:
            #    Completed = False; n = 0; nmax = 50
            #    try:
            #        while (not Completed) and n<=nmax:
            #            CommsData = Lta_Parse(packet.ReceivePacket(self.s))
            #            Completed = CommsData['CommsData']['Command']=='LtaGetComplete'
            #    except Exception as e:
            #        raise type(e)("Could not clear messages." + e.message)
            if type(e.args[0]) == dict:
                if type (e.args[0]['error out']) == OrderedDict:
                    print (type(e)('\033[91m'+"Fatal error: lta.__get__ command." + e.args[0]['error out']['source']))
            else:
                print(e)
    def __set__(self,arg,dataStruct):
        try:
            XMLData = Lta_Unparse({'SetData': OrderedDict([('Arg',arg),('Data',Lta_Unparse(dataStruct))])})
            cmdDict = Lta_Command('set',XMLData).cmdDict
            xml = Lta_Unparse(cmdDict);
            UsrTimeout = self.s.gettimeout()            
            self.s.settimeout(1)            
            packet.SendPacket(self.s,xml)
            self.s.settimeout(UsrTimeout)           
            Completed = False
            n = 0; nmax = 50
            #loop needed to receive all packages from LV
            while (not Completed) and n<=nmax:
                CommsData = packet.ReceivePacket(self.s)
                CommsData = Lta_Parse(CommsData);
                #print CommsData
                Completed = CommsData['CommsData']['Command']=='LtaSetComplete'
                if Completed:
                    NoError = Lta_Parse(CommsData['CommsData']['XMLData'])
                else:
                    Error = Lta_Parse(CommsData['CommsData']['XMLData'])
                n += 1
            
            if n>nmax:
                print( "Set was not acknowledged as completed")
            if n>1:
                return Error
            else:
                return NoError

        except (IOError, Exception) as e:
            #clear the messages before raising e
            print( "Got exception, clearing set command messages")
            Completed = False; n = 0; nmax = 50
            try:
                while (not Completed) and n<=nmax:
                    CommsData = Lta_Parse(packet.ReceivePacket(self.s))
                    Completed = CommsData['CommsData']['Command']=='LtaSetComplete'
            except Exception as e:
                raise type(e)("Could not clear messages." + e.message)
            raise type(e)("Fatal error: lta.__set__ command." + e.message)

    def __multirun__(self,ntries,secwait,ecode):
        #tries to run 'ntries' times if get error code 'ecode', waiting 'secwait' seconds before trying again
        #ecode is a set of error codes
        try:
            print( "Trying multiple runs")
            #time.sleep(3)  #wait some time before running
            Error = self.__run__()
            j = 1
            while (Error['error constant']['code'] in ecode) and j<=ntries:
                print( Error['error']['code'],"Error. ") #, Error['error']['source']
                print( "Trying again in", secwait, " seconds",)
                for k in range(1,secwait+1):
                    time.sleep(1)
                    print( ".",)
                print( "Try to run ", j+1)
                Error = self.__run__()
                j += 1
            if j>ntries:
                print( "Critical error: Run exceeded maximum allowed tries.")
                raise Exception("Critical error: Run exceeded maximum allowed tries.")
            else:
                return Error
        except (IOError, Exception) as e:
            raise type(e)("Fatal error: lta.__multirun__ command." + e.message)
    
    def __run__(self):
        try:
            cmdDict = Lta_Command('run',"").cmdDict
            xml = Lta_Unparse(cmdDict);
            packet.SendPacket(self.s, xml)
            Completed = False
            n = 0; nmax = 50
            #loop needed to receive all packages from LV
            while (not Completed) and n<=nmax:
                CommsData = packet.ReceivePacket(self.s)
                CommsData = Lta_Parse(CommsData);
                #print CommsData
                Completed = CommsData['CommsData']['Command']=='LtaRunComplete'
                if Completed:
                    NoError = Lta_Parse(CommsData['CommsData']['XMLData'])
                else:
                    Error = Lta_Parse(CommsData['CommsData']['XMLData'])
                n += 1
            
            if n>nmax:
                print( "Run was not acknowledged as completed")
            if n>1:
                return Error
            else:
                print( "Run complete")
                return NoError
            
        except (IOError, Exception) as e:
            #clear the messages before raising e
            print( "Got exception, clearing run command messages.")
            Completed = False; n = 0; nmax = 50
            try:
                while (not Completed) and n<=nmax:
                    CommsData = Lta_Parse(packet.ReceivePacket(self.s))
                    Completed = CommsData['CommsData']['Command']=='LtaRunComplete'
            except Exception as e:
                raise type(e)("Could not clear messages." + e.message)
            raise type(e)("Fatal error: lta.__run__ command." + e.message)

    def __runscriptuntiltimeout__(self,ScriptName,ntries,secwait,errorcode):
        #tries to run 'ntries' times if get error code 'errorcode', waiting 'secwait' seconds before trying again
        #ecode is a set of error codes
        try:
            Error = self.__runscript__(ScriptName)
            j = 1
            while j<=ntries and (Error['Error Out']['code'] in errorcode):
                if (j==1):
                    print( "Error " +str(Error['Error Out']['code'])+ " occured ")
                print( "Trying again in "+ str(secwait)+ " seconds")
                for k in range(1,secwait+1):
                    time.sleep(1)
                    print( str(k)+"seconds")
                
                if (j==ntries):
                    print("Last Attempt take " +str(j+1))
                else:
                    print( "Running again take "+str(j+1))
                    
                Error = self.__runscript__(ScriptName)
                j += 1
            if j>ntries and (Error['Error Out']['code'] in errorcode):
                print( "Critical error: Run exceeded maximum allowed tries.")
                raise Exception("Critical error: Run exceeded maximum allowed tries.")
            else:
                return Error                
        except (IOError, Exception) as e:
            raise type(e)("Fatal error: lta.__multirun__ command." + e.message)
    
    def __runscript__(self,ScriptName):
        """ for now, arg is the XML string of the run command """
        try:
            UsrTimeout = self.s.gettimeout()
            self.s.settimeout(1)  
            cmd = Lta_Command('run', ScriptName) 
            self.s.settimeout(UsrTimeout)                                                                                                                                                                                               
            xml = Lta_Unparse(cmd.cmdDict)
            packet.SendPacket(self.s,xml)
            Completed = False
            n = 0; nmax = 50
            #loop needed to receive all packages from LV
            while (not Completed) and n<=nmax:
                #time.sleep(.4)
                CommsData = packet.ReceivePacket(self.s)
                CommsData = Lta_Parse(CommsData);
                #print CommsData
                Completed = CommsData['CommsData']['Command']=='LtaRunComplete'
                if Completed:
                    NoError = Lta_Parse(CommsData['CommsData']['XMLData'])
                else:
                    Error = Lta_Parse(CommsData['CommsData']['XMLData'])    
                n += 1
            
            if n>nmax:
                print( "Run was not acknowledged as completed")
            if n>1:
                return Error
            else:
                print( "Run completed")
                return NoError
            
        except (IOError, Exception) as e:
            #clear the messages before raising e
            print( "Got exception, clearing run command messages.")
            Completed = False; n = 0; nmax = 50
            try:
                while (not Completed) and n<=nmax:
                    CommsData = Lta_Parse(packet.ReceivePacket(self.s))
                    Completed = CommsData['CommsData']['Command']=='LtaRunComplete'
            except Exception as e:
                raise type(e)("Could not clear messages." + e.message)
            raise type(e)("Fatal error: lta.__run__ command." + e.message)

if __name__=='__main__':
    try:
        #execfile(sys.argv[1])
        exec(open(sys.argv[1]).read())   # Python 3 deprecated execfile

    except Exception as ex:
        lta = Lta("127.0.0.1",60100)
        lta.connect()
        err = Lta_Error(ex,sys.exc_info())
        lta.send_error(err,3,'Abort')
        lta.close()



     
