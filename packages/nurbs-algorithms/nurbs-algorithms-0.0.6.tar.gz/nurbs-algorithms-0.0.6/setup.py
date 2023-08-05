from distutils.core import setup
from setuptools import find_packages

KEYWORDS = ['NURBS']
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3.6',
]


with open('__version__', 'r') as f:
    version = f.read().strip()


setup(
    name='nurbs-algorithms',
    version=version,
    description='nurbs-algorithms',
    author='Jeff Cochran',
    author_email='jeffrey.david.cochran@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
    ],
    url='https://github.com/jeffrey-cochran/nurbs-algorithms',
    download_url='https://github.com/jeffrey-cochran/nurbs-algorithms/archive/%s.tar.gz' % version,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
)
