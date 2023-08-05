from setuptools import setup, find_packages

print find_packages()
setup(name='xbos',
      version='0.0.18',
      description='Aggregate wrapper for XBOS services and devices',
      url='https://github.com/SoftwareDefinedBuildings/XBOS',
      author='Gabe Fierro',
      author_email='gtfierro@cs.berkeley.edu',
      packages=find_packages(),
      data_files=[('.', ['xbos/services/data.capnp'])],
      install_requires=[
        'delorean==0.6.0',
        'msgpack-python==0.4.2',
        'bw2python>=0.6.1',
        'requests>=2.12.2',
        'python-dateutil>=2.4.2',
        'pandas>=0.20.1'
      ],
      zip_safe=False)

