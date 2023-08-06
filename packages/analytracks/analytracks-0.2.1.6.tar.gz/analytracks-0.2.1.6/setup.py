from setuptools import setup

setup(name='analytracks',
      version='0.2.1.6',
      description='This python package contains tools to handle sport gps tracks',
      url='http://github.com/ddolbecke/analytracks',
      author='Dimitri de Smet',
      author_email='dimitri.desmet@uclouvain.be',
      license='MIT',
      packages=['analytracks'],
      package_data={'mypkg': ['data/*.dat']},
      zip_safe=True)
