import os
import shutil
import subprocess as sp
import sys

from setuptools import find_packages, setup

base_dir = os.path.dirname(__file__)


def remove_build_files():
    for f in ('build', 'dist', 'sqlwriter.egg-info'):
        if os.path.exists(f):
            shutil.rmtree(f)


with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()


def do_setup():
    remove_build_files()
    setup(
        name='sqlwriter',
        version='1.0.2',
        license="MIT",
        description="Writes pandas DataFrame to several flavors of sql database",
        long_description=long_description,
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            'pandas==0.21.0',
            'numpy==1.13.3'
        ],
        author='',
        author_email='',
        url='https://github.com/estenssors/sqlwriter',
        scripts=['sqlwriter/bin/sqlwriter'],
        entry_points={'console_scripts':
                      ['sqlwriter = sqlwriter.bin.sqlwriter:entrypoint']
                      },
    )


if __name__ == '__main__':
    do_setup()
