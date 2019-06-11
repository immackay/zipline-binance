from setuptools import setup

setup(
    name='zipline-binance',
    version='0.1.0',
    url='https://github.com/immackay/zipline-binance',
    license='Apache v2',
    author='Ian MacKay',
    author_email='immackay0@gmail.com',
    description='Binance Support for Zipline',
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    packages=['zipline_binance'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Financial :: Investment"
    ],
)
