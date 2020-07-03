import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ssds-claytsay',
    version='0.1.0',
    author='Clay Tsay',
    author_email='',
    description='Some specialized data structures for Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/claytsay/ssds-python',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache License 2.0',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
