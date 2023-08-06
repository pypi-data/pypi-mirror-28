from distutils.core import setup

from setuptools import setup, find_packages

PACKAGE = "ali_domain_sdk"
NAME = "ali_domain_sdk"
DESCRIPTION = "阿里域名解析SDK"
AUTHOR = "Mg_P"
AUTHOR_EMAIL = "w2xzzpig@hotmail.com"
URL = "https://github.com/xzzpig/AliDomainSDK"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="GNU General Public License v3.0",
    url=URL,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    zip_safe=False,
    requires=["requests"],
    install_requires=["requests"],
)