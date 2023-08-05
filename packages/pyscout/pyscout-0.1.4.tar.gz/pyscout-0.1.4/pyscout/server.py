import zmq
import os
from threading import Thread
from timekeeper_plot import timekeeper_plot



class pyscout_server():
    def __init__(self, zmq_port=2000, visdom_port = 4065):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.addr = 'tcp://*:%d'%zmq_port
        self.socket.bind(self.addr)
        self.socket.setsockopt(zmq.SUBSCRIBE, '')
        self.zmq_port = zmq_port
        self.visdom_port = visdom_port
        self.plots = {}

    def run_main_loop(self):
        self.zmq_thread = Thread(target=self.main_loop)
        self.zmq_thread.start()
        print('Pyscout server is running with zmq port set on %s' % self.addr)


    def main_loop(self):
        while True:
            name, val = self.socket.recv_pyobj()
            print(name,val)
            if name not in self.plots:
                new_plot = timekeeper_plot(name, visdom_port=self.visdom_port)
                self.plots.update({name : new_plot})
            self.plots[name].feed(val)

    def wait(self):
        self.zmq_thread.join()





if __name__ == '__main__':
    serv = pyscout_server()
    serv.run_main_loop()
