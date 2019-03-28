"""
---------------------------------------------------------------------------
NDarrayUtility.py
Kirk D Evans 07/2018 kdevans@fs.fed.us
    TetraTech EC for:
    USDA Forest Service
    Region 5 Remote Sensing Lab

script to: misc array (raster) functions

known limitations: python 3.x
---------------------------------------------------------------------------
"""
import numpy as np

def in_list(arr, lstVals):
    """ Return array arr with only values in lstVals, else 0
        numpy version of Spatial Analyst InList
    """
    arrOut = np.zeros(arr.shape)
    for v in lstVals:
        arrOut += np.where(arr == v, v, 0)

    return arrOut

def in_list_nan(arr, lstVals):
    """ Return array arr with only values in lstVals, else numpy.nan
        numpy version of Spatial Analyst InList
    """
    arrOut = np.zeros(arr.shape) * np.nan
    for v in lstVals:
        arrOut = np.where(arr == v, v, arrOut)

    return arrOut

# ---------------------------------------------------------------------------
# for Block statistics
def percent_over_h(arr, fltH):
    """ Return scalar describing the fraction of elements in arr
            that are greater than fltH.
    """
    arrMask = np.where(arr > fltH, 1, 0)
    return arrMask.sum() / arr.size

def mean_over_h(arr, fltH):
    """ Return scalar describing the mean of all those elements in arr
            that are greater than fltH.
    """
    arrGTf = (arr * (arr > fltH)).flatten()
    return arrGTf.take(arrGTf.nonzero()).mean()

if __name__ == "__main__":
    arrTest = np.array([[1, 2, -1], [4, 5, 1], [7, 8, -1]])
    print(arrTest)

    fltOverH = percent_over_h(arrTest, 2)
    fltMeanOverH = mean_over_h(arrTest, 2)

    print(fltOverH, fltMeanOverH)
