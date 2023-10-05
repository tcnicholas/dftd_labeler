from setuptools import setup, find_packages


setup(
    name='dftd_labeler',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'ase',
    ],
    entry_points={
        'console_scripts': [
            'dftd_labeler=dftd_labeler.labeler:main',
        ],
    },
    author='Thomas C Nicholas',
    author_email='thomas.nicholas@chem.ox.ac.uk',
    description='A convenience tool to label structures with DFT dispersion corrections.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tcnicholas/dftd_labeler',    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
