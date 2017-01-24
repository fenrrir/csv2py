# coding: utf-8

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))


setup(
    name='csv2py',
    version='0.0.1',
    description='Importa arquivo csv para objetos python.',
    url='https://github.com/fenrrir/csv2py',
    author=u'Rodrigo Pinheiro Marques de Araújo',
    author_email='fenrrir@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.9',
    ],
    keywords='python csv django',
    py_modules=['csv2py'],
    install_requires=['six==1.10.0'],
)

