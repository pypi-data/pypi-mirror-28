
import time

class wizzard():
    def __init__(self, name):
        print('init-%s'%name)
    def __enter__(self):
        print('enter')
    def __exit__(self, type, value, traceback):
        print('exit')


with wizzard('ddd'):
    time.sleep(2)