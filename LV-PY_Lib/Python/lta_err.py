# -*- coding: utf-8 -*-
"""
Exception classes for NIST Labview Test Automation (LTA)

Created on Sun Feb 26 10:11:32 2017
Revised on Tuesday, Oct 25 2022

@author: AR
"""
import sys
import traceback
from collections import OrderedDict

class Lta_Error(Exception):
    """ Error objects are created around python Exceptions and unparsed into
    LabVIEW XML error clusters including the error <err>, <b>Complete call chain</b>
    priority <pri>, and severity <sev> tags. """
    
    def __init__(self,origEx,origSysInfo):
        if not hasattr(origEx,'message'):
            if hasattr(origEx,'args'):
                origEx.message = origEx.args[0]
            else:
                origEx.message = ('error unknown: original Exception has no arguments')
        self.origEx = origEx
        self.origSysInfo = origSysInfo
        super(Lta_Error,self).__init__(origEx.message,)

    def __traceback__(self):
        """build the traceback call chain string"""
        tb = self.origSysInfo[2]
        tbList=traceback.extract_tb(tb)
        tbStr = ''
        for element in tbList:
            tbStr = tbStr + 'In line {0} of file {1}:\n{2}\n'.format(element[1],
                    element[0],element[-1])
        return tbStr
                    
    def __str__(self):
        tbStr = self.__traceback__()
        return 'error: {0}: {1}\nTraceback:\n{2}'.format(
            type(self.origEx).__name__,self.origEx,tbStr)


    def LvError(self,pri,sev):
        """ build a Labview error dictionary ready for unparsing to XML """

        Source = 'Python<ERR>\n'        
        Source = Source + str(self.origEx) + '\n\n<b>Complete call chain:<b>\n'
        Source = Source + self.__traceback__() + '\n'
        Source = Source + '<PRI>' + str(pri) + '\n<SEV>'+ sev + '\n'
#        errorDict['error out']['source']=Source
        errorDict = {'error out' : OrderedDict([('status',True),('code', 30000),('source', Source)])}
        
        return errorDict


class LV_to_Py_Error(Exception):
    """
    When an error comes from the labview side
    """
    def __init__(self, error, message="Error was received from LabVIEW: "):
        self.status = error['error out']['status']
        self.code = error['error out']['code']
        self.source = error['error out']['source']
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} code: {self.code}, source: {self.source}'


if __name__ =='__main__':
    import sys
    from lta_unparse import Lta_Unparse
    try:
        q = 1/0
    except Exception as e:
        err = Lta_Error(e,sys.exc_info())
        print( err)
        errorDict = err.LvError(3,'abort')
        print( 'errorDict:\n' + str(errorDict) + '\n')
        print( Lta_Unparse(errorDict))
        
        