# coding: utf-8

## Class to VisualMemoryException
# Class used to handle system errors
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
        elif numbererror == 3: # Detecting external kill
            print 'Process kill command detected'