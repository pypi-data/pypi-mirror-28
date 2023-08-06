from setuptools import setup

setup(
    name='sqlalchemy-vertica-python',
    version='0.2.1',
    description='Vertica dialect for sqlalchemy using vertica_python',
    long_description=open("README.rst").read(),
    license="MIT",
    url='https://github.com/LocusEnergy/sqlalchemy-vertica-python',
    download_url = 'https://github.com/LocusEnergy/sqlalchemy-vertica-python/tarball/0.2.1',
    author='Locus Energy',
    author_email='dbio@locusenergy.com',
    packages=[
        'sqla_vertica_python',
    ],
    entry_points="""
    [sqlalchemy.dialects]
    vertica.vertica_python = sqla_vertica_python.vertica_python:VerticaDialect
    """,
    install_requires=[
        'vertica_python'
    ],
)

