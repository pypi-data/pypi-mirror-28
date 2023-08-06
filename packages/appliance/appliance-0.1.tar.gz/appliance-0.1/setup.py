import os
from setuptools import find_packages, setup
 
setup(
    name='appliance',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django app to conduct Web-based appliances management.',
    
     
    author='Abhishek Kulkarni',
    author_email='abhisheksadanand89@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        
    ],
)
