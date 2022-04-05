from setuptools import setup

setup(
    name='pywsjtx',
    version='0.1.0',
    description='A python module to interpret and create WSJT-X UDP packets',
    url='https://github.com/bmo/py-wsjtx',
    author='Brian Moran',
    author_email='',
    license='MIT',
    packages=['pywsjtx','pywsjtx.extra'],
    install_requires=[],

    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
