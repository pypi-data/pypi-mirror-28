import os
import sys
from setuptools import setup, find_packages

version = __import__('fiber').__version__

if sys.argv[-1] == 'publish':  # upload to pypi
    os.system("python setup.py register sdist bdist_egg bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

setup(
    name='django-fiber',
    version=version,
    license='Apache License, Version 2.0',

    install_requires=[
        'Pillow>=2.2.1',
        'django-mptt>=0.9.0',
        'django_compressor>=2.2',
        'djangorestframework>=3.7.7',
        'easy-thumbnails>=2.5.0',
    ],

    description='Django Fiber - a simple, user-friendly CMS for all your Django projects',
    long_description=open('README.rst').read(),

    author='Dennis Bunskoek',
    author_email='dbunskoek@leukeleu.nl',

    url='https://github.com/django-fiber/django-fiber',

    packages=find_packages(),
    include_package_data=True,

    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
    ],
    keywords=['cms', 'django']
)
