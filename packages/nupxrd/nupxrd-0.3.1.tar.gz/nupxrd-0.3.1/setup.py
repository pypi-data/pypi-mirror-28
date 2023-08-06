from setuptools import setup

setup(name='nupxrd',
      version='0.3.1',
      description='Extract raw data from a .dat file generated on the XRD\
                   equipment',
      url='https://github.com/RossVerploegh/nupxrd/',
      license='MIT',
      author='Ross Verploegh',
      author_email='rverploe@alumni.nd.edu',
      packages=['nupxrd'],
      install_requires=[],
      download_url=('https://github.com/RossVerploegh/nupxrd/archive/0.3.1\
                     .tar.gz'),
      keywords=['powderXRD', 'MOF', 'NuMat'],  # arbitrary keywords
      include_package_data=True,
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Natural Language :: English",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Topic :: Scientific/Engineering :: Chemistry"
                   ]
      )
