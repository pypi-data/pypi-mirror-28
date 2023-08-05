from setuptools import setup, find_packages

setup(
    name='flashlight',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['flashlight = flashlight.backend.server:run']},)
