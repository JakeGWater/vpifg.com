#!/bin/sh

V1=$(sed -nE "s/^.*version.*=.*([0-9]+\.[0-9]+\.[0-9]+(\.[a-z0-9]+)?).*$/\1/p" setup.py)
V2=$(sed -nE "s/^.*version.*=.*([0-9]+\.[0-9]+\.[0-9]+(\.[a-z0-9]+)?).*$/\1/p" sphinxcontrib/images.py)
SUB=$(git submodule status sphinxcontrib_images_lightbox2/lightbox2 | cut -c1)

printf "\n## RELEASE SPHINXCONTRIB-IMAGES TO PYPI ##\n\n"
printf "Refer to the comments and commented out commands\n"
printf "in this script for one possible release procedure.\n\n"

printf "# VERSION CHECK #\n"
printf "setup.py: %s\n" "$V1"
printf "sphinxcontrib/images.py: %s\n" "$V2"

if [ "$V1" != "$V2" ]; then
    printf "ERROR: versions do _not_ match\n\n"
else
    printf "SUCCESS: Versions match\n\n"
fi

printf "# SUBMODULE STATUS #\n"
if [ "$SUB" = "-" ]; then
    echo "ERROR: lightbox2 submodule _not_ initialized"
else
    echo "SUCCESS: lightbox2 submodule initialized"
fi



## Prerequisites
## - Bump version in setup.py
## - Bump version in sphinxcontrib/images.py
## - Make sure the lightbox2 submodule is clone
##   (git submodule update --init --recursive)


## Create a virtual environment for twine installation
# python -m venv venv
# source venv/bin/activate
# pip install twine


## Create the distribution
# python setup.py sdist bdist_wheel


## Upload to TestPyPI to verify things look right
## Add '.preN' to the release number when testing (e.g. '0.9.3.pre1')
## https://test.pypi.org/account/register/ 
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*


## Upload to PyPI
## Remember to remove '.preN' from the version before rebuilding and uploading
## Requires user with maintainer status on the package/project
# twine upload dist/*
