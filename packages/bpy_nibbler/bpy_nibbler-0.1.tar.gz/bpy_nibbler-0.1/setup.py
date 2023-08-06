#!/usr/bin/env python

from setuptools import setup

setup(name='bpy_nibbler',
      version='0.1',
      description='A compiled binary of Blender-as-a-Python-Module (bpy) for use in AWS Lambda with cycles',
      author='John Martinez',
      author_email='johndavidmartinez1@gmail.com',
      url='https://github.com/johndavidmartinez/bpy_lambda',
      packages=['bpy_lambda'],
      include_package_data=True
      )
