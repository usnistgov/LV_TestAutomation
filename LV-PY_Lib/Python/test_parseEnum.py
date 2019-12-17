# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 17:23:05 2019

@author: gra1
"""

import sys, os
from lta_err import Lta_Error
from lta_parse import lta_parse

def getXML(fileRelPath):
    try:
        thisDir = os.getcwd();
        fileDir = os.path.join(thisDir,fileRelPath)  
        return open(fileDir).read()
    except Exception as e:
        raise e


if __name__=='__main__':
    try:
        xml=getXML('enumData.xml')
        top_dict=Lta_parse(xml)

    except Exception as e:
        a=Lta_Error(e,sys.exc_info())
        print a  
                