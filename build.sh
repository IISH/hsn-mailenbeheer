#!/bin/bash
#
# ./build.sh [instance] [version] [python distribution]
#
# Build script for the project to produce a packaged distribution.
#
# Example: ./build.sh hsn-mailenbeheer 1.0.0 /usr/share/python/2.7.10
#
# Requirements: virtualenv and pip must be installed with the targeted python distribution.

instance=$1
if [ -z "$instance" ] ; then
    instance="hsn-mailenbeheer"
    echo "Setting default instance to ${instance}"
fi

version=$2
if [ -z "$version" ] ; then
    version="1.0.0"
    echo "Setting default version to ${version} "
fi

p=$3
if [ -z "$p" ] ; then
    p=$(which python)
    echo "Setting default python to system ${p}"
fi


revision=$(git rev-parse HEAD)
echo "instance=${instance}"
echo "version=${version}"
echo "python distribution=${p}"
echo "revision=${revision}"



# Remove any precious builds
if [ -d target ] ; then
    rm -rf target
fi


# Create a workspace
work=$instance-$version
if [ -d $work ] ; then
	rm -rf $work
fi
rsync -av --progress --exclude='build.sh' --exclude='.git' . $work
echo $revision > $work/revision.txt


# Setup and activate a virtual environment
$p/bin/virtualenv $work/virtualenv
. $work/virtualenv/bin/activate


# Retrieve the dependencies
pip install -r $work/requirements.txt


# Test
python $work/server/manage.py test $work/server
rc=$?
if [ $rc -eq 0 ] ; then
    # ToDo: parse the test report
    mkdir -p "target/test-reports"
else
	echo -e "There are test failures."
	exit $rc
fi


# Build the java libraries
$work/client/hsnmailenbeheer/generate.py source
$work/client/hsnmailenbeheer/generate.py build


# Create the artifact
mkdir -p target
tar -pczf target/$instance-$version.tar.gz $work

exit 0