"""---------------------------------------------------------------------------
 poolTasks.py

 Kirk Evans, GIS Analyst, TetraTech EC @ USDA Forest Service R5/Remote Sensing Lab
   3237 Peacekeeper Way, Suite 201
   McClellan, CA 95652
   kdevans@fs.fed.us
   
 script to: task classes for pool2 module

 know limitations: python 3.x
---------------------------------------------------------------------------
"""
# task classes
class MP_Task:
    ''' Class to hold multiprocessing worker tasks.
        To be placed into MP_taskset.
    '''
    def __init__(self, func, args, comment = None):
        self.func = func
        self.args = args
        self.comment = comment

    def __str__(self):
        strPrint = 'MP_task: ' + self.func.__name__ + str(self.args)
        return strPrint

class MP_TaskSet:
    ''' Class to bundle MP_task instances. '''
    def __init__(self, comment = None):
        self.tasks = []
        self.count = 0
        self.comment = comment

    def addTask(self, task):
        self.tasks.append(task)
        self.count += 1

    def __str__(self):
        strPrint = 'MP_taskset: [' + ', '.join([t.func.__name__ for t in self.tasks]) + ']'
        return strPrint
