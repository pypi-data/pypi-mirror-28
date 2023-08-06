from setuptools import setup

setup(
    name='PowerFullSoap',
    version='0.3.0',
    description='PowerFullSoap',
	packages=['PowerFullSoap'],
    author='ahmetatakan',
    author_email='ahmetatakan79@gmail.com',
	classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
	install_requires=[
        "requests",
        "xmltodict",
		"dicttoxml",
        "tldextract",
        "lxml"
    ],
)