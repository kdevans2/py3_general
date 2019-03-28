"""
---------------------------------------------------------------------------
 poolResults.py

 Kirk Evans, GIS Analyst, TetraTech EC @ USDA Forest Service R5/Remote Sensing Lab
   3237 Peacekeeper Way, Suite 201
   McClellan, CA 95652
   kdevans@fs.fed.us
   
 script to: pool2 result classes

 know limitations: python 3.x
---------------------------------------------------------------------------
"""
import pickle
import general as gen

# ----------------------------------------
# result classes
class MP_Result:
    """ class to hold Multiprocessing worker results. Used by fWrap. """
    def __init__(self, strComment, args):
        self.ID = strComment # a comment or ID
        self.args = args
        self.result = None
        self.time = 0
        self.error = None
        
    def __str__(self):
        strT = gen.time_string(self.time)
        strPrint = self.ID + ", " + strT
        if self.error:
            strPrint += ', EXCEPTION: \n' + self.error
        return strPrint

class MP_ResultSet:
    """ Class to hold MP_Results. """
    def __init__(self, strID, intPID = None):
        self.results = []
        self.count = 0
        self.ID = strID # like old 'strComment'
        self.PID = intPID
        self.time = 0
        self.hasError = False

    def addResult(self, result):
        self.results.append(result)
        self.count += 1
        
    def __str__(self):
        strT = gen.time_string(self.time)
        strPrint = self.ID + ", " + strT
        if self.hasError:
            strPrint += ', EXCEPTION recorded.'
        return strPrint

class PoolResults:
    """ Class to hold multiprocessing resultset objects (MP_ResultSets) """
    def __init__(self, workers):
        """ init """
        self.workers = workers
        self.runtime = 0
        self.ResultSets = []
        self.Count = 0
        self.ErrorCount = 0

    def __len__(self):
        """ lenr method """
        return self.Count

    def __str__(self):
        """ str method """
        strText = 'PoolResult object\n\tWorkers: ' + str(self.workers) + \
                  '\n\tTaskSets: ' + str(self.Count) + \
                  '\n\tErrors: ' + str(self.ErrorCount) + \
                  '\n\tTime: ' + gen.time_string(self.runtime)
        return strText
    
    def record(self, resultset):
        """ """
        self.ResultSets.append(resultset)
        self.Count += 1
        if resultset.hasError:
            self.ErrorCount += 1

    def printErrors(self, listAll = False):
        """ """
        intDefaultList = 6
        if listAll == True:
            intDo = self.ErrorCount
        else:
            intDo = intDefaultList
        i = 0
        bolContinue = True
        for rs in self.ResultSets:
            for r in rs.results:
                if r.error:
                    print(rs)
                    print('\t' + str(r) + '\n')
                    i += 1
                    if i == intDo:
                        intRemaining = self.ErrorCount - intDo
                        if intRemaining:
                            print('Error descriptions limited to ' + str(intDo) + ' results.\n\t' + str(intRemaining) + ' reamining.')
                            bolContinue = False
            if not bolContinue:
                break
                
    def printResultsSets(self):
        """ """
        for rs in self.ResultSets:
            print('\t' + rs.ID) 
            for r in rs.results:
                print('\t' + r.ID + ': ' + str(r.result))

    def listOutputs(self, intResultSetIndex = None):
        """ """
        if not intResultSetIndex is None:
            intIndex = intResultSetIndex
            return [rs.results[intIndex].result for rs in self.ResultSets]
        else:
            return [[r.result for r in rs.results] for rs in self.ResultSets]

    def Pickle(self, strTXT):
        """ Go pickle (your)self """
        with open(strTXT, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def listPIDs(self):
        """ Retrun list of uniqie PIDs from result set objects. """
        return list(set([rs.PID for rs in self.ResultSets]))
