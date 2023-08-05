#   Copyright 2015-2016 See CONTRIBUTORS.md file
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from setuptools import setup, find_packages
setup(
    name='accloudtant',
    packages=find_packages(),
    version='0.1.4',
    description='Cloud cost calculation tool',
    author='Ignasi Fosch, Eduardo Bellido Bellido, David Arcos',
    author_email='accloudtant@y10k.ws',
    url='https://github.com/ifosch/accloudtant',
    download_url='https://github.com/ifosch/accloudtant/archive/0.1.4',
    keywords=['cloud', 'AWS', 'costs'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Office/Business :: Financial :: Investment',
    ],
    install_requires=['requests', 'tabulate', 'click', 'boto3'],
    scripts=['bin/accloudtant'],
)
