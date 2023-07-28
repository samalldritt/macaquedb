from setuptools import setup, find_packages

setup(
    name='macaquedb',
    version='1.0.0',
    description='SQLite Database interface for PRIME-DE data',
    author='Sam Alldritt',
    author_email='samuel.alldritt@childmind.org',
    url='https://github.com/samalldritt/macaquedb',
    packages=find_packages(),
    install_requires=[
        'pandas==1.5.3'
    ]
)
