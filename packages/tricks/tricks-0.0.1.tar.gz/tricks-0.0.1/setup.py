## -------------------------------------------------------------------
##
## Copyright (c) 2018 Vitor Enes. All Rights Reserved.
##
## This file is provided to you under the Apache License,
## Version 2.0 (the "License"); you may not use this file
## except in compliance with the License.  You may obtain
## a copy of the License at
##
##   http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing,
## software distributed under the License is distributed on an
## "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
## KIND, either express or implied.  See the License for the
## specific language governing permissions and limitations
## under the License.
##
## -------------------------------------------------------------------

from setuptools import find_packages, setup

# Do not edit these constants. They will be updated automatically
# by scripts/update-client.sh.
CLIENT_VERSION = "0.0.1"
PACKAGE_NAME = "tricks"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

with open('requirements.txt') as f:
    REQUIRES = f.readlines()

setup(
    name=PACKAGE_NAME,
    version=CLIENT_VERSION,
    description="tricks python client",
    author_email="vitorenesduarte@gmail.com",
    author="Vitor Enes",
    license="Apache License Version 2.0",
    url="https://github.com/vitorenesduarte/tricks-client",
    keywords=["Kubernetes", "Deployment", "Experiments", "Tricks"],
    install_requires=REQUIRES,
    packages=find_packages()
)
