# ---------------------------------------------------------------------------
# pool3.py
# Kirk Evans 7/18 TetraTech EC
# script to: DoPool and supporting functions
#   result classes moved to poolResults.py
#   task classes moved to poolTasks.py
#
# Added functionality:
#   priority.Priority() allows user to control thread niceness (priority)
#
# know limitations: python 3.x
#   This version uses priority module, which uses psutil
# ---------------------------------------------------------------------------
import traceback, sys, os, time, multiprocessing, pickle, subprocess
import general as g
import poolResults as poolR
from poolTasks import *
import priority

# ---------------------------------------------------------------------------
# worker and wrapper functions
def _worker(qInput, qOutput, iPriority):
    ''' Worker function placed into queue. '''

    intPID = iPriority.SetNiceness()
        
    for TS in iter(qInput.get, 'STOP'):
        R = _fWrap(TS, iPriority, intPID)
        qOutput.put(R)

def _fWrap(TaskSet, iPriority, intPID):
    ''' Wrapper for passed functions.
        Organizes results, timing and exceptions into MP_ResultSet objects.
    '''
    try:
        iResultSet = poolR.MP_ResultSet(TaskSet.comment, intPID)
        t0 = time.time()
        
        for task in TaskSet.tasks:
            iResult = poolR.MP_Result(task.comment, task.args)
            t1 = time.time()
            
            # call function
            args = task.args
            f = task.func
            r = f(*args)
            iResult.result = r
            iResult.time = time.time() - t1
            iResultSet.addResult(iResult)

    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        strTrace = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print(strTrace)
        iResult.error = strTrace
        iResultSet.addResult(iResult)
        iResultSet.hasError = True
        
    finally:
        # record timing and return resultset object.
        iResultSet.time = time.time() - t0
        return iResultSet

def Range(i):
    ''' dummy test function '''
    return range(i)

def test_args(a, b= '2'):
    ''' dummy  *args test function '''
    time.sleep(a/2)
    return str(a) + str(b)

def submit(cmd, output = None):
    ''' Submit a command to the command prompt.
        Optional output will be checked for existance if given and returned if true.
    '''
    # if output exists, skip cmd and return output 
    if output and os.path.exists(output):
        print('Output already present.')
        return output
        
    r = os.system(cmd)
    if output:
        if not os.path.exists(output):
            raise Exception('Output not created: ' + output)
        return output
    else:
        if r:
            raise Exception('Nonzero exit status.')
        return 'submit'

def POpen(cmd, output = None):
    ''' Submit a command via subprocess.Popen.
        Optional output will be checked for existance if given and returned if true.
        --- NOT working! ---
    '''
    # if output exists, skip cmd and return output 
    if output and os.path.exists(output):
        return output
        
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    if output:
        if not os.path.exists(output):
            raise Exception('Output not created: ' + output + '\nmessage:\n' + out)
        return output
    else:
        return 'POpen'


# ---------------------------------------------------------------------------                    
def DoPool(lstTasks, intWorkers, txtPickle = None, iPriority = priority.Priority()):
    ''' Run tasksets in lstTasks over intWorkers workers using multiprocessing.Process.
        Return PoolResults object.
    '''
    # Create queues and result object
    print('\n\tStart Pool:')
    print('\t\t' + str(len(lstTasks)) + ' task(s).')
    t0 = time.time()
    task_queue = multiprocessing.Queue()
    done_queue = multiprocessing.Queue()
    iPoolResult = poolR.PoolResults(intWorkers)

    # Submit tasks
    for task in lstTasks:
        task_queue.put(task)

    # Start worker processes
    print('\t\t' + str(intWorkers) + ' worker(s).')
    for intWorker in range(intWorkers):
        multiprocessing.Process(target=_worker, args=(task_queue, done_queue, iPriority)).start()
    
    # Get and print results
    print('\t\tUnordered results:')
    for i in range(len(lstTasks)):
        resultSet = done_queue.get()
        print('\t\t\t' + str(resultSet))
        iPoolResult.record(resultSet)

    # Tell child processes to stop
    for i in range(intWorkers):
        task_queue.put('STOP')

    iPoolResult.runtime = time.time() - t0

    if iPoolResult.ErrorCount:
        print('\n\t\tPool done: WITH ERRORS!.\n')
    else:
        print('\n\t\tPool done: ' + g.time_string(iPoolResult.runtime) + '\n')

    if txtPickle:
        iPoolResult.Pickle(txtPickle)
        
    return iPoolResult
