import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-url-simplify',
    version='0.0.1',
    packages=['url_simplify'],
    include_package_data=True,
    license='MIT License',
    description='A simple Django app to generate simplified urls.',
    long_description=README,
    url='https://www.example.com/',
    author='Aleksandr Kurlov',
    author_email='sasha.kurlov@gmail.com',
    install_requires=['django>=2.0', 'shortuuid'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
