from setuptools import setup, find_packages

setup(
    name="Jyxml",
    author="Gurkirat Singh",
    author_email="tbhaxor@gmail.com",
    version="0.1.0",
    description="A simple python module for JSON - XML - YAML parsing.",
    url="https://tbhaxor.github.io/jyxml",
    download_url="https://github.com/tbhaxor/jyxml/archive/master.zip",
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='jyxml tbhaxor gurkirat singh',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['dicttoxml', 'xmltodict'],
    python_requires='>=3',

)
