import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='almvotes',
    version='1.2',
    packages=['almvotes', 'almvotos'],
    description='Libreria para el almacenamiento de los votos en la BD',
    long_description=README,
    author='Equipo almacenamiento',
    author_email='juasanpar@hotmail.com',
    download_url='https://github.com/Proyecto-EGC-G1/Almacenamiento-Votos-EGC-G1/tree/master/project/AlmacenamientoVotos',
    license='MIT',
    install_requires=[
        'Django>=1.4',
    ]
)
