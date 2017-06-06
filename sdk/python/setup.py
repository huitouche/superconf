from setuptools import setup, find_packages
  
PACKAGE = "superconf"  
NAME = "superconf"  
AUTHOR = "veficos"  
AUTHOR_EMAIL = "veficos@gmail.com"  
URL = "https://github.com/huitouche/superconf"  
VERSION = __import__(PACKAGE).__version__  
  
setup(  
    name=NAME,  
    version=VERSION,  
    author=AUTHOR,  
    author_email=AUTHOR_EMAIL,  
    license="GNU General Public License v3.0",  
    url=URL,  
    packages=["superconf"],  
    classifiers=[  
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Communications",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Networking",
    ],  
    install_requires = ["kazoo==2.3.1", "simplejson==3.10.0"],
    zip_safe=False,  
)
