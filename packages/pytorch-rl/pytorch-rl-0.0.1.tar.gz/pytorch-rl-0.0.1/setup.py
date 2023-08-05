from setuptools import setup
from setuptools import find_packages

setup(name='pytorch-rl',
      version='0.0.1',
      description='Reinforcement Learning using PyTorch',
      author='Khushhall Chandra Mahajan, Pulkit Katdare ',
      author_email='kcm00000@gmail.com, radiantpulkit@gmail.com',
      url='https://github.com/khushhallchandra/pytorch-rl',
      license='MIT',
      install_requires=['numpy', 'torch'],
      packages=find_packages())
