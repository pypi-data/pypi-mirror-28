from distutils.core import setup

def read(fname):
    with open(fname) as f:
        return f.read()

setup(
    name='coverage_shield',
    packages=['coverage_shield'],
    version='1.0',
    description='Uploads total coverage for displaying badge',
    long_description=read('README'),
    install_requires=['coverage'],
    author='Samuel Carlsson',
    author_email='samuel.carlsson@volumental.com',
    url='https://github.com/Volumental/badges',
    keywords=['coverage', 'badge', 'shields.io'],
)
