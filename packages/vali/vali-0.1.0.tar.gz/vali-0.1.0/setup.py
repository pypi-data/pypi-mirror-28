from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# with open(path.join(here, 'readme.md'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name='vali',
    version='0.1.0',
    description='Easy Type Checking',
    # long_description=long_description,
    url='https://github.com/llamicron/vali',
    author='Luke Sweeney',
    author_email='llamicron@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='validation type-checking type',
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    py_modules=["vali"]
    # install_requires=[],
)
