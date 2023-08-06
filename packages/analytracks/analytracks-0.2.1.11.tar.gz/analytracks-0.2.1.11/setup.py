from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='analytracks',
      version='0.2.1.11',
      description='This python package contains tools to handle sport gps tracks (tcx, gpx, ...)',
#      long_description=readme(),
      url='http://www.olbecke.eu/research',
      author='Dimitri de Smet',
      author_email='dimitri.desmet@uclouvain.be',
      license='MIT',
      packages=['analytracks'],
      install_requires=['pandas'],
      package_data={'mypkg': ['data/*.dat']},
      data_files=[('googleapikey', ['data/googleElevationApi.key'])],
      zip_safe=True)
