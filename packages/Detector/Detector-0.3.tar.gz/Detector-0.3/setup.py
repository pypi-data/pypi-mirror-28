from setuptools import setup, find_packages
PACKAGE = "Detector"
NAME = "Detector"
DESCRIPTION = "vunerable rsa keys detector"
AUTHOR = "Cao Pei"
AUTHOR_EMAIL = "970379828@qq.com"
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
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'Detector = Detector.detector:main',
        ],
    }
)
