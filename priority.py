# ---------------------------------------------------------------------------
# priority.py
# Kirk Evans 6/18 TetraTech EC
# script to: psultil process priority functions
#
# know limitations: python 3.x
# ---------------------------------------------------------------------------
import psutil

class Priority():
    ''' Class to contain psutil Process niceness and ioniceness. '''
    def __init__(self, strNice = 'normal', strIONice = 'normal'):
        self.strNice = strNice.lower()
        self.strIONice = strIONice.lower()

        if self.strNice == 'below':
            self._Nice = psutil.BELOW_NORMAL_PRIORITY_CLASS
        elif self.strNice == 'normal':
            self._Nice = psutil.NORMAL_PRIORITY_CLASS
        elif self.strNice == 'above':
            self._Nice = psutil.ABOVE_NORMAL_PRIORITY_CLASS
        elif self.strNice == 'high':
            self._Nice = psutil.HIGH_NORMAL_PRIORITY_CLASS
        elif self.strNice == 'realtime':
            self._Nice = psutil.REALTIME_NORMAL_PRIORITY_CLASS
        else:
            raise Exception('Unknown Niceness code. Use: "below", "normal", "above", "high", "realtime"')

        if self.strIONice == 'verylow':
            self._IONice = 0
        if self.strIONice == 'low':
            self._IONice = 1
        if self.strIONice == 'normal':
            self._IONice = 2
        else:
            raise Exception('Unknown IONiceness code. Use: "low", "verylow", "normal"')
        
    def SetNiceness(self):
        p = psutil.Process()
        print('SetNice, pid:' + str(p.pid))
        p.nice(self._Nice)

        return p.pid

    def ReSetNiceness(self):
        p = psutil.Process()
        print('ReSetNice, pid:' + str(p.pid))
        p.nice(psutil.NORMAL_PRIORITY_CLASS)
        
    def SetIONiceness(self):
        p = psutil.Process()
        print(p.pid)
        p.ionice(self._IONice)

    def ReSetIONiceness(self):
        p = psutil.Process()
        p.nice(2)

if __name__ == "__main__":
    pass
