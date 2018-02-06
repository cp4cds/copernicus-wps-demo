import os

from setuptools import setup, find_packages

version = __import__('copernicus').__version__
here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

reqs = [line.strip() for line in open('requirements/deploy.txt')]

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
]

setup(name='copernicus',
      version=version,
      description='WPS processes for copernicus wps demo',
      long_description=README + '\n\n' + CHANGES,
      classifiers=classifiers,
      author='Carsten Ehbrecht',
      author_email='ehbrecht@dkrz.de',
      url='https://github.com/cehbrecht/copernicus-wps-demo',
      license="Apache License v2.0",
      keywords='wps pywps conda birdhouse esmvaltool ncl copernicus',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='copernicus',
      install_requires=reqs,
      entry_points={
          'console_scripts': [
              'copernicus=copernicus:main'
          ]
      },

      )
