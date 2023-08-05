import os
from setuptools import setup


def long_description():
    path = os.path.join(os.path.dirname(__file__), 'README.rst')
    with open(path) as f:
        return f.read()


setup(name='cw_msgpack_coder',
      version='1.1.3',
      description='Simple and fast Python any object serialization with use msgpack.',
      long_description=long_description(),
      author='Cezary K. Wagner',
      author_email='Cezary.Wagner@gmail.com',
      url='https://github.com/ChameleonRed/cw_msgpack_coder',
      license='MIT',
      packages=['cw_msgpack_coder'],
      install_requires='u-msgpack-python',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'],
      keywords="msgpack serialization streaming object encoding decoding",
      test_suite="tests.test_umsgpack_coder")
