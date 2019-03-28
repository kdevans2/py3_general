"""
---------------------------------------------------------------------------
 general.py
    
 Kirk Evans, GIS Analyst/Programmer, TetraTech EC @ USDA Forest Service R5/Remote Sensing Lab
   3237 Peacekeeper Way, Suite 201
   McClellan, CA 95652
   kdevans@fs.fed.us

 module of commonly used utility functions
---------------------------------------------------------------------------
"""
import time
import glob
import os
import math

def print2(s, txt, boolQuiet = True):
    """ Print with write to text, print suppressed by default. """
    with open(txt, 'a') as t:
        t.write(s.strip() + '\n')
        
    if not boolQuiet:
        print(s)
        
# ---------------------------------------------------
# time
def elapsed_time(t):
    """ Return a string of format 'hh:mm:ss', representing time elapsed between
        establishing variable t (generally: t = time.time()) and funcion call.

        Result rounded to nearest second by time_string.
    """
    return time_string(time.time() - t)

def time_string(t):
    """ Return a string of format 'hh:mm:ss', representing time t in seconds 
        Result rounded to nearest second.
    """
    seconds = int(round(t))
    h,rsecs = divmod(seconds,3600)
    m,s = divmod(rsecs,60)
    return str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)

def elapsed_sec(t, intRound = 1):
    """ Return a string representing seconds elapsed between
        establishing variable t (generally: t = time.time()) and funcion call.

        Result rounded to intRound decimal places.
    """
    return str(round(time.time() - t, intRound))
# ---------------------------------------------------
# classes
class progressor:
    def __init__(self, intTotalCount, intBreaks, bolLineFeed = False):
        self.count = 0
        self.total = intTotalCount
        self.breaks = intBreaks
        self.increment = int(float(intTotalCount) / intBreaks)
        self.Feed = bolLineFeed

    def call(self):
        self.count += 1
        if not self.count % self.increment:
            strPrint = int(round(100 * float(self.count) / self.total))
            if self.Feed:
                print(strPrint)
            else:
                print(strPrint)
                #print(strPrint, end=' ')

# ---------------------------------------------------
# file system and paths
def formatPath(input_string):
    """ function to correct backslash issues in paths
        usage: strPath = ut.formatPath(strPath)
    """
    
    lstReplace = [["\a","/a"],
                  ["\b","/b"],
                  ["\f","/f"],
                  ["\n","/n"],
                  ["\r","/r"],
                  ["\t","/t"],
                  ["\v","/v"],
                  ["\\","/"]]

    # replce each type of escape
    for old, new in lstReplace:
        input_string = input_string.replace(old, new)

    return input_string

def DeleteIntermediatesGlob(lstDel):
    """ Function to delete list of files using the os.
        Not tested for all possible ancilary files: pyramids, xmls...
    """
    for f in lstDel:
        try:
            for d in glob.glob(os.path.splitext(f)[0] + '.*'):
                os.remove(d)
        except Exception:
            print(f + ' delete failed, skipping.')

# ---------------------------------------------------
# math
def point_sep(xy1, xy2):
    ''' Function to return the distance between two x,y pairs.
        inputs are either two strings consisting of a pair of space separated values (as returned from the shape.centroid property)
            or two lists, each of an x,y pair
        A float is returned.
    '''
    if type(xy1) == type(xy2) == type([]):
        x1, y1 = xy1[0], xy1[1]
        x2, y2 = xy2[0], xy2[1]
    elif type(xy1) == type(xy2) == type(""):
        x1, y1 = xy1.split(" ")
        x2, y2 = xy2.split(" ")
        x1 = float(x1)
        y1 = float(y1)
        x2 = float(x2)
        y1 = float(y1)
    else:
        raise Exception("Non matching input types: " + repr(xy1) + " and " + repr(xy2))
    
    return _pointSep(x1, y1, x2, y2)
    

def _pointSep(x1, y1, x2, y2):
    ''' function to return the distance between two x,y pairs.
        A float is returned.
    '''
    return math.sqrt(pow((x2-x1),2) + pow((y2-y1), 2))


# ---------------------------------------------------
# misc        
def Return(a):
    ''' Return input. '''
    return a

def Lower(s):
    ''' Return string s all lowercase '''
    return s.lower()

def Upper(s):
    ''' Return string s all uppercase '''
    return s.upper()
