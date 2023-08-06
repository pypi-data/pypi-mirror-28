import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='repoPruebaAlmVotes',
    version='1.1',
    packages=['almvotes', 'almvotos'],
    description='Libreria para el almacenamiento de los votos en la BD',
    long_description=README,
    author='Equipo almacenamiento',
    author_email='juasanpar@hotmail.com',
    download_url='https://github.com/danrodagu/repoPrueba',
    license='MIT',
    install_requires=[
        'Django>=1.4',
    ]
)
