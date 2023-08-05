#!/usr/bin/env python
from setuptools import setup
    
setup(name='mujpy',
      version='1.0.1',
      description='A Python MuSR data analysis graphical interface based on classes, designed for jupyter.',
      author='Roberto De Renzi, Pietro Bonfa',
      author_email='roberto.derenzi@unipr.it',
      url='https://github.com/RDeRenzi/mujpy',
      packages=['mujpy',
                'mujpy.aux',
                'mujpy.logo',
                'mujpy.mucomponents',
                'mujpy.musr2py',
                ],
      include_package_data=True,
      package_dir={'mujpy': 'mujpy' },
      install_requires=[
            'numpy >= 1.6',
            'ipywidgets >= 7.0',
            'iminuit >= 1.2',
            'matplotlib >= 2.0'
      ],
)
