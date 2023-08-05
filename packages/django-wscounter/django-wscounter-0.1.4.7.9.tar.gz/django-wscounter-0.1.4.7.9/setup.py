import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-wscounter',
    version='0.1.4.7.9',
    packages=['wscounter'],
    description='A dynamic web-socket',
    long_description=README,
    author='Firas Al Kafri',
    author_email='firas.alkafri@gmail.com',
    url='https://github.com/salalem/django-wscounter/',
    license='GPLv2',
    install_requires=[
        'Django>=1.8.18, <=1.9.2',
        'djangorestframework>=3.2.3, <=3.6.2',
        'cerberus>=1.1'
    ]
)
