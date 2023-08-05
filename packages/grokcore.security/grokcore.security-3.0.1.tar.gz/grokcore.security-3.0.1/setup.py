from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt')
    )

tests_require = [
    'grok',
    'grokcore.view[test]',
    'zope.app.wsgi',
    'zope.configuration',
    'zope.securitypolicy',
    'zope.testing',
    ]

setup(
    name='grokcore.security',
    version='3.0.1',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://grok.zope.org',
    download_url='http://pypi.python.org/pypi/grokcore.security',
    description='Grok-like configuration for Zope security components',
    long_description=long_description,
    license='ZPL',
    classifiers=['Intended Audience :: Developers',
                 'Development Status :: 6 - Mature',
                 'License :: OSI Approved :: Zope Public License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 ],
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'grokcore.component >= 2.1',
        'martian >= 0.13',
        'setuptools',
        'zope.component',
        'zope.dottedname',
        'zope.interface',
        'zope.security',
        ],
    tests_require=tests_require,
    extras_require={
        'role': [
            'zope.securitypolicy',
            ],
        'test': tests_require
        },
)
