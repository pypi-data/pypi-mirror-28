import os.path

from setuptools import setup, find_packages

version = '3.0.0'


detailed = open(
    os.path.join('src', 'megrok', 'strictrequire', 'README.txt')).read()


changes = open('CHANGES.txt').read()


long_description = '\n\n'.join([detailed, changes, ''])


tests_require = [
    'zope.component',
    'zope.interface',
    'zope.securitypolicy',
    'zope.testing',
    ]


setup(
    name='megrok.strictrequire',
    version=version,
    description=(
        'Checks that all grokked "view-like" components '
        'require a permission.'),
    long_description=long_description,
    classifiers=[],
    keywords=[],
    author='The Health Agency',
    author_email='techniek@thehealthagency.com',
    url='http://www.thehealthagency.com',
    license='ZPL 2.1',
    package_dir={'': 'src'},
    namespace_packages=['megrok'],
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'martian',
        'grok >= 3.0',
        ],
    extras_require={
        'test': tests_require
        },
    tests_require=tests_require,
    entry_points={},
    )
