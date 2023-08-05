import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-wscounter',
    version='0.1.3.4',
    packages=['wscounter'],
    description='A dynamic web-socket',
    long_description=README,
    author='Firas Al Kafri',
    author_email='firas.alkafri@gmail.com',
    url='https://github.com/salalem/django-wscounter/',
    license='GPLv2'
)
