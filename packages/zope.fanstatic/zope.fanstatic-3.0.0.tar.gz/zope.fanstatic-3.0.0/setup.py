import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('src/zope/fanstatic/README.txt')
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )


setup(
    name='zope.fanstatic',
    version='3.0.0',
    description="Fanstatic integration for Zope.",
    long_description=long_description,
    keywords='',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    url='http://pypi.python.org/pypi/zope.fanstatic',
    license='ZPL 2.1',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Zope3',
        ],
    packages=find_packages('src'),
    namespace_packages=['zope'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'fanstatic >= 1.0.0',
        'setuptools',
        'zope.component',
        'zope.errorview [browser]',
        'zope.event',
        'zope.interface',
        'zope.publisher',
        'zope.traversing',
        ],
    extras_require={
        'test': [
            'zope.annotation',
            'zope.app.appsetup',
            'zope.app.publication',
            'zope.app.wsgi[test]',
            'zope.browserpage',
            'zope.container',
            'zope.principalregistry',
            'zope.security',
            'zope.securitypolicy',
            'zope.site',
            'zope.testbrowser',
            ],
    },
)
