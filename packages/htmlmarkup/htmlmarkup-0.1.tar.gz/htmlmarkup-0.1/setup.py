import htmlmarkup

from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='htmlmarkup',
    version=htmlmarkup.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    test_suite='test'
)