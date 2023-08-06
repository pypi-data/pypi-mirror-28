from setuptools import setup

setup(name='analytracks',
      version='0.2.1.5',
      description='The funniest joke in the world',
      url='http://github.com/ddolbecke/analytracks',
      author='Dimitri de Smet',
      author_email='dimitri.desmet@uclouvain.be',
      license='MIT',
      packages=['analytracks'],
      package_data={'mypkg': ['data/*.dat']},
      zip_safe=True)
