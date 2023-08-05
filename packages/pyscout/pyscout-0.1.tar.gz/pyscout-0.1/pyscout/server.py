import visdom
import numpy as np
import time
from threading import Timer




class timekeeper_plot():
    def __init__(self, name='', refresh=0.1, period=1):
        self.name = name
        self.refresh = refresh
        self.period = period
        self.vals_lifo = []
        self.tt_lifo = []
        self.vis = visdom.Visdom()
        self.is_running = False
        self.start_time = time.time()
        self.win = None
        self.start()

    def feed(self, val):
        self.vals_lifo.append(val)
        self.tt_lifo.append(time.time())
        while time.time()-self.tt_lifo[0] > self.period:
            self.vals_lifo.pop(0)
            self.tt_lifo.pop(0)

    def plot(self):
        print(self.vals_lifo[-1])
        xx = np.array(self.tt_lifo)-self.start_time
        yy = np.array(self.vals_lifo)
        if self.win is None:
            opts = {'title': self.name, 'markersize':1}
            self.win = self.vis.line(X=xx, Y=yy, opts=opts)
        else:
            self.vis.updateTrace(X=xx, Y=yy, win=self.win, append=False)

    def _run(self):
        self.is_running = False
        self.start()
        self.plot()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.refresh, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False



if __name__ == '__main__':
    mooing = timekeeper_plot('test', 0.03, 1)
    for ii in range(1000):
        mooing.feed(np.random.randn())
        time.sleep(0.03)