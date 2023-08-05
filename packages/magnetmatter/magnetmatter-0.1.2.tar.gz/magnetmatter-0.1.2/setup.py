# setup.py

from distutils.core import setup
import os

setup(
    name='magnetmatter',
    version='0.1.2',
    packages=['magnetmatter',os.path.join('magnetmatter','modules')],
    license='MIT',
    author='Pelle Garbus',
    author_email='garbus@inano.au.dk',
    description='Visualization of neutron and X-ray powder diffraction FullProf-refined data',
    long_description=open('README.txt').read(),
    install_requires=["numpy","pandas","matplotlib"],
    url = 'https://github.com/pgarbus/magnetmatter',
)
