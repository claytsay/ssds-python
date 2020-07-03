import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ssds',
    version='0.1.1',
    author='Clay Tsay',
    author_email='',
    description='Some specialized data structures for Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/claytsay/ssds-python',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
