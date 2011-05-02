#!/usr/bin/env python

from distutils.core import setup

setup(name="django-co-connector",
      version="0.1",
      description="An extension to the Django web framework provides externalized group objects based on JRA5-T2 VO protocol development and COIP",
      author="Leif Johansson",
      author_email="leifj@nordu.net",
      url="http://github.com/leifj/django-co-connector",
      #download_url="",
      zip_safe=False,
      packages=["django_co_connector","django_co_acls"],
      package_dir={"": "src"},
      #package_data = {"django_user_channels": []},
      classifiers=["Development Status :: 3 - Alpha",
                   "Environment :: Web Environment",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Framework :: Django",])
