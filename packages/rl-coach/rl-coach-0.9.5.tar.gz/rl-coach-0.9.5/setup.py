#
# Copyright (c) 2017 Intel Corporation
#
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

import sys
from codecs import open
from os import path

from setuptools import setup, find_packages

sys.path.insert(0, path.join(path.dirname(__file__), 'rl_coach'))
from version import VERSION

# Creating the pip package involves the following steps:
# - Check that everything works fine by:
# 1. Create a new virtual environment using `virtualenv coach_env -p python3`
# 2. Run `python setup.py install`
# 3.

# - If everything works fine, build and upload the package to PyPi:
# 1. Update the version in coach/version.py
# 2. Remove the directories build, dist and rl_coach.egg-info if they exist
# 3. Run `python setup.py sdist`
# 4. Run `twine upload dist/*`


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='rl-coach',
    version=VERSION,
    description='Reinforcement Learning Coach enables easy experimentation with state of the art Reinforcement Learning algorithms.',
    url='https://github.com/NervanaSystems/coach',
    author='Intel AI Lab',
    author_email='coach@intel.com',
    packages=find_packages(),
    python_requires=">=3",
    install_requires=[
        'annoy==1.8.3', 'Pillow==4.3.0', 'matplotlib==2.0.2', 'numpy==1.13.0', 'pandas==0.20.2',
        'pygame==1.9.3', 'PyOpenGL==3.1.0', 'scipy==0.19.0', 'scikit-image==0.13.0',
        'box2d==2.3.2', 'gym==0.9.4', 'tensorflow-gpu==1.4.0'],
    extras_require={
        'dashboard': ['bokeh==0.12.6', 'futures==3.1.1', 'pandas==0.20.2', 'wxPython==4.0.0b2'],
        'neon': ['nervananeon']
    },
    package_data={'rl_coach': ['*.css', 'environments/*.ini']},
    entry_points={
        'console_scripts': [
            'coach=rl_coach.coach:main',
            'dashboard=rl_coach.dashboard:main'
        ],
    },
)