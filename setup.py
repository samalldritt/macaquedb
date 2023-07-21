from setuptools import setup, find_packages

setup(
    name='macaquedb',
    version='0.1.0',
    description='SQLite Database interface for PRIME-DE data',
    author='Sam Alldritt',
    author_email='samuel.alldritt@childmind.org',
    url='https://github.com/samalldritt/MacaqueDB',
    packages=find_packages(),
    install_requires=[
        'libgcc-ng>=11.2.0',
        'libgomp>=11.2.0',
        'ncurses>=6.4',
        'readline>=8.2',
        'sqlite>=3.40.1',
        'zlib>=1.2.13'
    ]
)

