from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mathstats',
    version='0.2.6.3',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        #"License :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Mathematics"
      ],
    #scripts=['README.md'],
    description='Statistical functions, goodness-of-fit tests and special and special distributions not implemented in scipy/numpy .',
    author='Kristoffer Sahlin',
    author_email='kristoffer.sahlin@scilifelab.se',
    url='https://github.com/ksahlin/mathstats',
    license='GPLv3',
    long_description=long_description,  # Optional,
    install_requires=['scipy>=0.9']
    #                  'networkx>=1.4'],
    #platforms=['Unix', 'Linux', 'Mac OS']
)
