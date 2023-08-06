"""Setup module."""

from setuptools import setup
from setuptools import find_packages
from pip.req import parse_requirements

REQS = [str(ir.req) for ir in parse_requirements(
    'requirements.txt', session='hack')]
REQS2 = [str(ir.req) for ir in parse_requirements(
    'dev-requirements.txt', session='hack')]


with open('VERSION') as _file:
    VERSION = _file.read()


setup(
    name='sonic182_logger',
    version=VERSION,
    description='Logger utilities',
    author='Johanderson Mogollon',
    author_email='johanderson@mogollon.com.ve',
    packages=find_packages(exclude=["tests"]),
    license='MIT',
    setup_requires=['pytest-runner'],
    test_requires=['pytest'],
    install_requires=REQS,
    extras_require={
        'dev': REQS2,
        'test': ['pytest', 'coverage']
    }
)
