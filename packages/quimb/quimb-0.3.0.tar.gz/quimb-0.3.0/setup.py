from setuptools import setup, find_packages
import versioneer

setup(
    name='quimb',
    description='Quantum information and many-body library.',
    url='http://quimb.readthedocs.io',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Johnnie Gray',
    license='MIT',
    packages=find_packages(exclude=['deps', 'tests*']),
    install_requires=[
        'numpy>=1.10',
        'scipy>=0.15',
        'numba>=0.22',
        'numexpr>=2.3',
        'psutil>=4.3.1',
        'cytoolz>=0.8.0',
    ],
    extras_require={
        'test': [
            'coverage',
            'pytest',
            'pytest-cov',
        ],
        'docs': [
            'sphinx',
            'sphinx_bootstrap_theme',
        ],
        'advanced_solvers': [
            'slepc4py',
        ],
        'tensor': [
            'opt_einsum',
            'matplotlib',
        ]
    },
    scripts=['bin/quimb-mpi-python'],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='quantum dmrg tensor',
)
