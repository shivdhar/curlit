from pathlib import Path

from setuptools import setup

reqs_file = Path('requirements.in')
reqs = reqs_file.read_text().splitlines()


setup(
    name='curlit',
    version='0.1',
    packages=['curlit'],
    url='https://github.com/shivdhar/curlit',
    license='MIT',
    author='Shiv Dhar',
    author_email='shiv.dhar@gmail.com',
    description='Curl your HTTP!',

    install_requires=reqs,
)
