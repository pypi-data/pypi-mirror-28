import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='iesugrace-django-polls',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',  # example license
    description='A simple Django app to conduct Web-based polls.',
    long_description=README,
    url='https://github.com/iesugrace/iesugrace-django-polls',
    download_url='https://github.com/iesugrace/iesugrace-django-polls/archive/0.2.tar.gz',
    author='iesugrace',
    author_email='iesugrace@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
