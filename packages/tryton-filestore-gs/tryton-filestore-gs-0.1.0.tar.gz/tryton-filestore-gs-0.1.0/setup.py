# This file is part of filestore-gs. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import os
import io
from setuptools import setup


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()

setup(name='tryton-filestore-gs',
    version='0.1.0',
    author='B2CK',
    author_email='info@b2ck.com',
    description='Store Tryton files on Google Cloud Storage',
    url='https://hg.b2ck.com/tryton-filestore-gs',
    long_description=read('README'),
    py_modules=['tryton_filestore_gs'],
    platforms='Posix; MacOS X; Windows',
    keywords='tryton google cloud storage',
    classifiers=[
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        ],
    license='GPL-3',
    install_requires=[
        'google-cloud-storage',
        'trytond > 4.2',
        ],
    use_2to3=True,
    )
