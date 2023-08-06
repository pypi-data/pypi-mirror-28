#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import warnings
import re
from setuptools import setup, find_packages
import sys
import os

if sys.version_info.major == 3:
    from urllib3 import disable_warnings
    disable_warnings()

#with warnings.catch_warnings():
#    if not sys.version_info.major == 3:
    #    sys.exit("\n \
#        print('*********************************************************************') 
#        print('* The CLI is primarly tested for Python 3 but Python 2 should work. *')
#        print('* If you see issues with Python 2, Please email help@pipeline.ai    *')
#        print('*********************************************************************')

with warnings.catch_warnings():
    version = re.search(
            '^__version__\s*=\s*"(.*)"',
            open('cli_pipeline/cli_pipeline.py').read(),
            re.M
        ).group(1)


# Get the long description from the relevant file
with warnings.catch_warnings():
    with open('README.rst') as f:
        long_description = f.read()

with warnings.catch_warnings():
    requirements_path = './requirements.txt'    
    requirements_path = os.path.normpath(requirements_path)
    requirements_path = os.path.expandvars(requirements_path)
    requirements_path = os.path.expanduser(requirements_path)
    requirements_path = os.path.abspath(requirements_path)

    with open(requirements_path) as f:
        requirements = [line.rstrip() for line in f.readlines()]

with warnings.catch_warnings():
    setup(
        include_package_data=True,
        name = "cli-pipeline",
        packages = ["cli_pipeline"],
        entry_points = {
            "console_scripts": ['pipeline = cli_pipeline.cli_pipeline:_main']
        },
        version = version,
        description = "PipelineAI CLI",
        long_description = "%s\n\nRequirements:\n%s" % (long_description, requirements),
        author = "Chris Fregly",
        author_email = "github@pipeline.ai",
        url = "https://github.com/PipelineAI/",
        install_requires=requirements,
        dependency_links=[],
        package=find_packages(exclude=['concurrent', 'concurrent.*', '*.concurrent.*']),
    )
