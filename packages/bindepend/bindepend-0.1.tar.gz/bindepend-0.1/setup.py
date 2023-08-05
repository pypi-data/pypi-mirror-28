
import os

from setuptools import setup, find_packages

setup(
    name='bindepend',
    description='Binary depedency analysis',
    author='Mars Galactic',
    author_email='xoviat@users.noreply.github.com',
    url='https://github.com/xoviat/bindepend',
    py_modules=['bindepend'],
    license='GNU GPLv3',
    platforms='any',
    keywords=['pyinstaller'],
    requires_python=">=3.3",
    install_requires=[
        'pefile'
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    use_scm_version=True)
