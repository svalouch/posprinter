
from setuptools import setup

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='posprinter',
    version='0.0.1',
    author='Stefan Valouch',
    author_email='svalouch@valouch.de',
    description='Library for interacting with Point Of Sales (POS) printers',
    long_description=long_description,
    packages=['posprinter'],
    package_data={'posprinter': ['py.typed']},
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='BSD-3-Clause',
    url='https://github.com/svalouch/posprinter',
    platforms='any',
    python_requires='>=3.5',

    install_requires=[
        'pyserial>=3.4',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
        'docs': [
            'Sphinx>=2.0',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
