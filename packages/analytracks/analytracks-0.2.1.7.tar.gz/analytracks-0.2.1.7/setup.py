from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='analytracks',
      version='0.2.1.7',
      description='This python package contains tools to handle sport gps tracks (tcx, gpx, ...)',
      long_description=readme(),
      url='http://github.com/ddolbecke/analytracks',
      author='Dimitri de Smet',
      author_email='dimitri.desmet@uclouvain.be',
      license='MIT',
      packages=['analytracks'],
      package_data={'mypkg': ['data/*.dat']},
      zip_safe=True)
