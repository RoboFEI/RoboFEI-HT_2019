# coding: utf-8

#  ****************************************************************************
#  * @file: VisualMemoryException.py
#  * @project: ROBOFEI-HT - FEI 😛
#  * @author: Vinicius Nicassio Ferreira
#  * @version: V0.0.1
#  * @created: 23/10/2017
#  * @e-mail: vinicius.nicassio@gmail.com
#  * @brief: Class VisualMemoryException
#  ****************************************************************************

# ---- Imports ----

# Libraries to be used.
import sys

## Class VisualMemoryException
# Class used to handle system errors.
class VisualMemoryException(Exception):
    
    ## Constructor Class
    # Displays the error message.
    def __init__(self, numbererror, message):
        self.numbererror = numbererror
        if numbererror == 5: # Request to terminate processes by one of the threads.
            print 'Request process termination by thread', message
            return
        print 'Vision Memory System Error:',
        if numbererror == 0: # Generic error messages
            print message
        elif numbererror == 1: # Number of robots incoherent
            print "Number of robots incoherent, it was not possible to use \""+ str(message) +"\" robots in field."
            sys.exit(1)
        elif numbererror == 3: # Detecting external kill
            print 'Process kill command detected'