import zmq
import time


class aggregator():
    def __init__(self, port):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect('tcp://*:2000')
        self.socket.setsockopt(zmq.SUBSCRIBE, '')

    def run_main_loop(self):
        while True:
            message = self.socket.recv_pyobj()
            print(message)




class logger():
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.connect('tcp://localhost:2000')
        print('Logger initilized.')
    def log(self, msg):
        self.socket.send_pyobj(msg)
        print(msg)


class timekeeper():
    def __init__(self, name):
        self.name = name
        self.start_time = time.time()
    def __enter__(self):
        pass
        #print('enter')
    def __exit__(self, type, value, traceback):
        end_time = time.time()
        tt = time.time()
        global _logger_instance
        #import ipdb; ipdb.set_trace()
        try:
            _logger_instance.log((self.name, end_time - self.start_time))
        except:
            _logger_instance = logger()
            _logger_instance.log((self.name, end_time - self.start_time))
        print(time.time()-tt)

if __name__ == '__main__':
    for ii in range(100):
        with timekeeper('test'):
            time.sleep(0.1)