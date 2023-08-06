from setuptools import setup, find_packages

def read(fname):
    return open(fname).read()

setup(
    name="dbcalc",
    version="0.1.3",
    author="Vieler Hyloks",
    author_email="vielerhyloks@gmail.com",
    description="A dB <-> power calculator for the command line",
    long_description=read('README.rst'),
    url="https://bitbucket.org/Vieler/dbcalc/",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dbcalc = dbcalc:main'
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Physics"
    ]
)
