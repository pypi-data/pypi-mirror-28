import os
from setuptools import setup, find_packages

version = '3.0.0'


install_requires = [
    'Chameleon >= 2.10',
    'grokcore.component',
    'grokcore.view',
    'setuptools',
    'z3c.pt >= 2.2.2',
    'zope.i18n',
    ]


tests_require = [
    'grokcore.viewlet',
    'zope.app.appsetup',
    'zope.app.wsgi',
    'zope.testbrowser',
    ]


long_description = (
    open('README.txt').read() +
    '\n\n' +
    open(os.path.join('src', 'grokcore', 'chameleon', 'README.txt')).read() +
    '\n\n' +
    open('CHANGES.txt').read())


setup(
    name='grokcore.chameleon',
    version=version,
    description="Chameleon page template support for Grok",
    long_description=long_description,
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
    keywords="grok chameleon template",
    author="Uli Fouquet",
    author_email="grok-dev@zope.org",
    url="http://pypi.python.org/pypi/grokcore.chameleon",
    license="ZPL",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    )
