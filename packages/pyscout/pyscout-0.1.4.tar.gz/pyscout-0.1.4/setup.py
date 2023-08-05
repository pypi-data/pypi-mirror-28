from setuptools import setup

setup(name='pyscout',
      version='0.1.4',
      description='Realtime monitoring and benchmarking code execution',
      url='https://github.com/agatetx/pyscout.git',
      author='agatetx',
      author_email='agatetx@gmail.com',
      license='MIT',
      packages=['pyscout'],
      install_requires=['zmq', 'visdom'],
      scripts=['bin/run-pyscout-server'],
      zip_safe=False)