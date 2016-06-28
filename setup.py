from setuptools import setup, find_packages


setup(
    name="pbviewer",
    packages=['pbviewer'],
    version="0.1.0",
    include_package_data=True,
    description='Protocol Buffers Inspector',
    url='https://github.com/onesuper/pbviewer',
    author='onesuper',
    test_suite = 'nose.collector',
    tests_require=['nose', 'protobuf'],
)



