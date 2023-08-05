import os
import shutil

from setuptools import find_packages, setup

base_dir = os.path.dirname(__file__)

for f in ('build', 'dist', 'sebflow.egg-info'):
    if os.path.exists(f):
        shutil.rmtree(f)

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

def do_setup():
    setup(
        name='sebflow',
        version='0.0.1',
        license='MIT',
        description='programatically author and monitor data pipelines',
        long_description=long_description,
        packages=find_packages(),
        include_package_data =True,
        install_requires=[
            'psycopg2==2.7.3.2',
            'django==1.11',
            'tabulate==0.7.7',
            'sqlalchemy-utc==0.9.0',
            'termcolor==1.1.0',
            'colorama==0.3.9'
        ],
        author='Sebastian Estenssoro',
        author_email='seb.estenssoro@gmail.com',
        url='https://github.com/estenssoros/sebflow',
        scripts=['sebflow/bin/sebflow'],
        entry_points={'console_scripts':
                      ['sebflow = sebflow.bin.sebflow:entrypoint']
                      },
    )


if __name__ == '__main__':
    do_setup()
