from setuptools import find_packages, setup

with open('bessie/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

with open('README.md', 'rb') as f:
    readme = f.read().decode('utf-8')

REQUIRES = ['requests']

setup(
    name='bessie',
    version=version,
    description='Bessie - Base API Client',
    long_description=readme,
    author='Andrew Henry',
    author_email='andymitchhank@users.noreply.github.com',
    maintainer='Andrew Henry',
    maintainer_email='andymitchhank@users.noreply.github.com',
    url='https://github.com/andymitchhank/bessie',
    license='MIT',

    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    install_requires=REQUIRES,
    tests_require=['coverage', 'pytest'],

    packages=find_packages(),
)
