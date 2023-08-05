from distutils.core import setup

setup(
    # Application name:
    name="pg_to_brokers",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Duc Dinh",
    author_email="minhduccm90@gmail.com",

    # Packages
    packages=["pg_to_brokers"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/minhduccm/pg_to_brokers",

    # license="LICENSE.txt",
    description="A light weight python package to stream data changes from PostgeSQL to popular Brokers such as Kinesis, ...",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "psycopg2",
        "boto"
    ],
)
