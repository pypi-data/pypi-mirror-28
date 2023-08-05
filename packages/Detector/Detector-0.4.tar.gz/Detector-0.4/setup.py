from setuptools import setup, find_packages
PACKAGE = "Detector"
NAME = "Detector"
DESCRIPTION = "vunerable rsa keys detector"
AUTHOR = "Cao Pei"
AUTHOR_EMAIL = "970379828@qq.com"
install_requires = [
    'cryptography',
    'setuptools>=1.0',
    'six',
    'future',
    'coloredlogs',
    'pgpdump',
    'python-dateutil',
]
#URL = ""
VERSION = __import__(PACKAGE).__version__
 
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description="My test module",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    #url=URL,
    packages=find_packages(),

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    python_requires='>=2.7.10,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    install_requires=install_requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'Detector = Detector.detector:main',
        ],
    }
)
