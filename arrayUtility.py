'''
---------------------------------------------------------------------------
arrayUtilities.py
Kirk D Evans 07/2018 kdevans@fs.fed.us
    TetraTech EC for:
    USDA Forest Service
    Region 5 Remote Sensing Lab

script to: misc array and list function

know limitations: python 3.x
---------------------------------------------------------------------------
'''
import sys, os
import numpy as np
import general as g
sys.path.append(os.path.abspath('.'))

def indexCuts(intLen, intBreaks):
    ''' Return a list of list/array indeces describing the
            cut points of an iterable of length intLen
            into intBreaks slices of approximately equal length.
    '''
    if type(intLen) != int:
        raise Exception('arg: intLen, must be integer')
    if type(intLen) != int:
        raise Exception('arg: intBreaks, must be integer')
    if intBreaks < 1:
        raise Exception('arg: intBreaks, must be greater than 0')
    
    intwidth = float(intLen)/intBreaks
    lstCuts = [0]
    
    for i in range(1,intBreaks):
        lstCuts.append(int(round(i * intwidth)))
    lstCuts.append(intLen)
    
    return lstCuts


def tupCuts(lstC):
    ''' Return list of tuples given lstC of length n:
        [(lstC[0], lstC[1]), (lstC[1], lstC[2]), (lstC[0], lstC[1])..., (lstC[n-2], lstC[n-1])]
    '''
    return [(lstC[i], lstC[i+1]) for i in range(len(lstC) - 1)]


def splitSample(lst, tupBreak, bolMakeArray = True, fTransform = g.Return):
    ''' Given tupBreak (i,j), return two lists:
            lstSubset =  lst[i:j]
            lstRest = lst[:i] + lst[j:], i.e. arr without lstIn
        Optionally convert lstIn and lstOut to numpy arrays
        Optionally apply function fTransform to elements of lstIn and lstOut
    '''
    if type(lst) not in (list, tuple):
        raise Exception('arg: lst, must be list or tuple')
    
    i, j = tupBreak
    lstSubset =  lst[i:j]
    lstRest = lst[:i] + lst[j:]

    if bolMakeArray:
        return fTransform(np.array(lstSubset)), fTransform(np.array(lstRest))
    else:
        return [fTransform(k) for k in lstSubset], [fTransform(k) for k in lstRest]
    
if __name__ == "__main__":
    pass
    

