from setuptools import setup

setup(
    name="authhub",
    version='0.0.1',
    packages=['authhub', 'authhub.providers'],
    install_requires=[
        'masonite',
        'requests'
    ],
    include_package_data=True,
)
