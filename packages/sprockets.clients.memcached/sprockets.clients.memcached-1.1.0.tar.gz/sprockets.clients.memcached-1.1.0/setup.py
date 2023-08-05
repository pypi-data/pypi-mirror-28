import codecs
import sys

import setuptools


def read_requirements(name):
    requirements = []
    with open(name) as req_file:
        for line in req_file:
            if '#' in line:
                line = line[:line.index('#')]
            requirements.append(line.strip())
    return requirements


setuptools.setup(
    name='sprockets.clients.memcached',
    version='1.1.0',
    description=('Memcached client wrapper that is configured via '
                 'environment variables'),
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    url='https://github.com/sprockets/sprockets.clients.memcached.git',
    author='AWeber Communications',
    author_email='api@aweber.com',
    license=codecs.open('LICENSE', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 5 - Production',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['sprockets',
              'sprockets.clients',
              'sprockets.clients.memcached'],
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
    namespace_packages=['sprockets', 'sprockets.clients'],
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('test-requirements.txt'),
    zip_safe=False)
