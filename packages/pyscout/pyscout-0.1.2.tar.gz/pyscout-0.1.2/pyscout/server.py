import zmq
from timekeeper_plot import timekeeper_plot




class pyscout_server():
    def __init__(self, port=2000):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect('tcp://*:%d'%port)
        self.socket.setsockopt(zmq.SUBSCRIBE, '')

        self.plots = {}

    def run_main_loop(self):
        while True:
            name, val = self.socket.recv_pyobj()
            if name not in self.plots:
                new_plot = timekeeper_plot(name)
                self.plots.update({name : new_plot})
            self.plots[name].feed(val)






if __name__ == '__main__':
    serv = pyscout_server()
    serv.run_main_loop()
