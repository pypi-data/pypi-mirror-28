import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-salalem_utils',
    version='0.1.2.2',
    packages=['salalem_utils'],
    description='Salalem Django Utilities and Extensions',
    long_description=README,
    author='Firas Al Kafri',
    author_email='firas.alkafri@gmail.com',
    url='https://github.com/salalem/django-salalem_utils/',
    license='GPLv2',
    install_requires=[
        'Django<2',
        'django-extensions'
    ]
)
