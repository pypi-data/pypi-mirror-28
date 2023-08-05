from setuptools import setup, find_packages

setup(
    name='communardo-metadata',
    packages=find_packages(),
    version='0.2.0',
    description='A simple wrapper around the Communardo Metadata REST API.',
    author='David Tyler',
    author_email='davet.code@gmail.com',
    url='https://github.com/DaveTCode/communardo-metadata-python-lib',
    keywords=['communardo', 'metadata'],
    classifiers=[],
    setup_requires=['pytest-runner'],
    install_requires=['requests >= 2.18.4, < 3.0.0a0'],
    tests_require=['pytest >= 3.0.7, < 4.0.0a0', 'pytest-cov >= 2.5.0, < 3.0.0a0']
)
