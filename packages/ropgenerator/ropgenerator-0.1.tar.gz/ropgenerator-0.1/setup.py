from setuptools import setup, Command
import os

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vr ./build ./*.pyc ./*.tgz ./*.egg-info')

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='ropgenerator',
      version='0.1',
      description='ROPGenerator makes ROP exploits easy by finding and chaining gadgets',
      url='',
      author='Boyan MILANOV',
      author_email='boyan.milanov@hotmail.fr',
      license='MIT',
      classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 2.7',
      'Topic :: Security',	
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      ],
      packages=['ropgenerator'],
      install_requires=['ROPGadget', 'barf'],   
      dependency_links=['https://github.com/Z3Prover/z3/tree/master/src/api/python'],
      keywords='ROP chain gadget semantic automatic exploit',  
      zip_safe=False, 
      cmdclass={
        'clean': CleanCommand,
      }
      
    )
      
     
