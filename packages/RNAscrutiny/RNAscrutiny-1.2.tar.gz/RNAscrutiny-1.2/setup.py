from setuptools import setup

setup(
    name='RNAscrutiny',
    version='1.2',
    description='Tool for simulating and analyzing single-cell RNA-sequencing data.',
    keywords=
    'RNA single cell simulation inference generative genomics transcriptomics',
    url='http://lbm.niddk.nih.gov/mckennajp/scRutiNy',
    author='Joseph P McKena',
    author_email='joseph.mckenna@nih.gov',
    license='MIT',
    packages=['RNAscrutiny'],
    install_requires=['numpy', 'matplotlib', 'sklearn'],
    zip_safe=False)
