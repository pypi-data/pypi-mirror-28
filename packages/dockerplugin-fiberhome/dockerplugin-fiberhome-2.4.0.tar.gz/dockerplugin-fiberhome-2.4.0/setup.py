# ============LICENSE_START=======================================================
# org.onap.dcae
# ================================================================================
# Copyright (c) 2017 AT&T Intellectual Property. All rights reserved.
# ================================================================================
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============LICENSE_END=========================================================
#
# ECOMP is a trademark and service mark of AT&T Intellectual Property.

import os
from setuptools import setup

setup(
    name='dockerplugin-fiberhome',
    description='Cloudify plugin for applications run in Docker containers,revised by FiberHome',
    version="2.4.0",
    author='Michael Hwang, Tommy Carpenter,Minglu Li',
    packages=['dockerplugin'],
    zip_safe=False,
    install_requires=[
        "python-consul>=0.6.0,<1.0.0",
        "onap-dcae-dockering-fiberhome==1.4.1",
        "uuid==1.30",
        "onap-dcae-dcaepolicy-lib>=1.0.0"
    ]
)
