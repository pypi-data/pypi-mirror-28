import visdom
import numpy as np
import time
from threading import Timer




class timekeeper_plot():
    def __init__(self, name='', refresh=0.1, period=1, visdom_port=8097):
        self.name = name
        self.refresh = refresh
        self.period = period
        self.vals_lifo = []
        self.tt_lifo = []
        self.vis = visdom.Visdom(port = visdom_port)
        self.is_running = False
        self.start_time = time.time()
        self.win = None
        self.start()
        self.ymax = None
        self.ymax_alpha = 0.01

    def feed(self, val):
        self.vals_lifo.append(val)
        self.tt_lifo.append(time.time())
        while time.time()-self.tt_lifo[0] > self.period:
            self.vals_lifo.pop(0)
            self.tt_lifo.pop(0)

    def plot(self):
        #print(self.vals_lifo[-1])
        xx = np.array(self.tt_lifo)-self.start_time
        yy = np.array(self.vals_lifo)
        if self.ymax is None:
            self.ymax = yy.max()
        else:
            self.ymax = (1-self.ymax_alpha)*self.ymax + self.ymax_alpha*yy.max()
        opts = {'title': self.name, 'markersize':1, 'ytickmin' : 0, 'ytickmax' : self.ymax}
        if self.win is None:
            self.win = self.vis.line(X=xx, Y=yy, opts=opts)
        else:
            self.vis.line(X=xx, Y=yy, win=self.win, update='replace', opts=opts)
        #    self.vis.updateTrace(X=xx, Y=yy, win=self.win, append=False)

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