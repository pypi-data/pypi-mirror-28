# Copyright 2017-2018 cardinfolink, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

classifiers = """
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: Apache Software License
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Topic :: Database
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Unix
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
"""

from distutils.core import setup

setup(
    name='mongox-doc-manager',
    version='0.0.6',
    packages=["mongo_connector", "mongo_connector.doc_managers"],
    url='https://github.com/hongmi/mongox-doc-manager',
    license='http://www.apache.org/licenses/LICENSE-2.0.html',
    classifiers=list(filter(None, classifiers.split("\n"))),
    author='hongmin',
    author_email='hongmix@gmail.com',
    description='a mongo-connector doc manager, make target collection can treat as a stream'
)
