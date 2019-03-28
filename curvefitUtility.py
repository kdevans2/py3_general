# ---------------------------------------------------------------------------
# curvefitUtilities.py
# Kirk Evans 6/18 TetraTech EC
# module to: curve fitting and supporting functions
#
# know limitations: python 3.x
# ---------------------------------------------------------------------------
import numpy as np
from numpy import log as ln
import os, sys, math
from scipy.optimize import curve_fit

# ---------------------------------------------------------------------------
# Curtis-Arney functional forms [4.1.1]
# All functions assume height in feet and dbh in inches.
def CurtAr_DBH_fOf_H(H, P2, P3, P4):
    return ((ln((H-4.5)/P2))/-P3) ** (1/P4)

def CurtAr_H_fOf_DBH(DBH, P2, P3, P4):
    return  4.5 + P2 * np.exp(-P3 * DBH ** P4)

# Wykoff functional forms [4.1.2]
def Wyk_DBH_fOf_H(H, B1, B2):
    return B2 / (ln(H-4.5) - B1) -1

def Wyk_H_fOf_DBH(DBH, B1, B2):
    return 4.5 + np.exp(B1 + B2 / (DBH + 1.0))


# ---------------------------------------------------------------------------
# Fitting functions
def Fit_CurtAr(arrHT, arrDBH, p = (500,5,-0.1), maxFEV = 1000000):
    ''' Fit coefficients for Curtis-Arney functional form DBH = f(HT).
        Return coefficients popt_CurtAr and predicted DBH arrDBH_predCurtAr.
    '''
    popt_CurtAr, pcov_CurtAr = curve_fit(CurtAr_DBH_fOf_H, arrHT, arrDBH, p0 = p, maxfev = maxFEV)
    arrDBH_predCurtAr = CurtAr_DBH_fOf_H(arrHT, *popt_CurtAr)
    
    return popt_CurtAr, arrDBH_predCurtAr

def Fit_Wyk(arrHT, arrDBH, p = (5,-1)):
    ''' Fit coefficients for Wykoff functional form DBH = f(HT).
        Return coefficients popt_Wyk and predicted DBH arrDBH_predWyk.
    '''
    popt_Wyk, pcov_Wyk = curve_fit(Wyk_DBH_fOf_H, arrHT, arrDBH, p0 = p, maxfev=1000000)
    arrDBH_predWyk = Wyk_DBH_fOf_H(arrHT, *popt_Wyk)
    
    return popt_Wyk, arrDBH_predWyk

def Fit_General(arrX, arrY, fFit, p, maxFEV = 1000000):
    ''' '''
    print('\tCurve fitting. Form: ' + fFit.__name__)
    popt, pcov = curve_fit(fFit, arrX, arrY, p0 = p, maxfev = maxFEV)
    arrY_pred = fFit(arrX, *popt)
    
    return popt, arrY_pred


# ---------------------------------------------------------------------------
# Goodness of fit functions
def SER(arObserv, arPred):
    ''' '''
    if not len(arObserv) == len(arPred):
        raise Exception("Array lengths don't match")
    
    n = len(arObserv)
    arRes_sqrd = (arObserv - arPred)**2
    return math.sqrt(arRes_sqrd.sum() / n)

def COD(arObserv, arPred):
    ''' '''
    if not len(arObserv) == len(arPred):
        raise Exception("Array lengths don't match")
    
    SStot = ( (arObserv - arObserv.mean()) ** 2 ).sum()
    SSres = ( (arObserv - arPred) ** 2 ).sum()
    return 1 - SSres/SStot


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    pass
    

