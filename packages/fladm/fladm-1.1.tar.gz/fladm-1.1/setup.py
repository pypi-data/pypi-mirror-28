import io
from setuptools import find_packages, setup


# Read in the README for the long description on PyPI
def long_description():
    return 'description'
    # with io.open('README.rst', 'r', encoding='utf-8') as f:
    #     readme = f.read()
    # return readme

setup(name='fladm',
      version='1.1',
      description='Flamingo admin cli tool',
      long_description=long_description(),
      url='http://gitlab.exem-oss.org/flamingo/flamingo-adm-cli.git',
      author='Jaeik Park',
      author_email='jaeikpark81@gmail.com',
      license='Apache2',
      packages=find_packages(),
      install_requires=['paramiko'],
      entry_points = {
        'console_scripts': ['fladm=fladm.cli:main']
      },
      package_data={'': ['*.json']},
      classifiers=[
          'Programming Language :: Python :: 2.7'
      ],
      zip_safe=False)

# from distutils.core import setup
#
# py_modules = [
#  'paramiko'
# ]
# print 'Flamingo-cli modules\n%s' % py_modules
#
# setup (name = 'Flamingo-cli',
#        version = '1.0',
#        description = 'This is a flamingo development cli tool',
#        py_modules = py_modules)