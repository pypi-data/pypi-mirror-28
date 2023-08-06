from setuptools import find_packages
from setuptools import setup

import os.path


version = '1.3.1'

setup(
    name='Products.i18ntestcase',
    version=version,
    description="Products.i18ntestcase is build on top of the ZopeTestCase "
                "package. It has been developed to simplify testing of "
                "gettext i18n files for Zope products.",
    long_description=(open("README.txt").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.txt")).read()),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Plone i18n gettext testcase',
    author='Hanno Schlichting',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://github.com/plone/Products.i18ntestcase',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      'setuptools',
      'six',
    ],
)
