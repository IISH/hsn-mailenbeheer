#!/bin/bash
#
# ./build.sh [instance] [version] [workspace] [python distribution]
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

workspace=$3
if [ -z "$workspace" ] ; then
    workspace="/home/${instance}"
    echo "Setting default workspacespace to ${workspace}"
fi

p=$4
if [ -z "$p" ] ; then
    p=$(which python)
    echo "Setting default python to system ${p}"
fi


revision=$(git rev-parse HEAD)
echo "instance=${instance}"
echo "version=${version}"
echo "workspacespace=${workspace}"
echo "python distribution=${p}"
echo "revision=${revision}"



# Remove any previous builds
if [ -d target ] ; then
    rm -rf target
fi


# Create a workspace
if [ -d $workspace ] ; then
    rm -rf $workspace/*
fi
rsync -av --progress --exclude='build.sh' --exclude='.git' . $workspace
echo $revision > $workspace/revision.txt


# Setup and activate a virtual environment
$p/bin/virtualenv $workspace/virtualenv
. $workspace/virtualenv/bin/activate


# Retrieve the dependencies
pip install -r $workspace/requirements.txt --cache-dir=/tmp


# Build the javascript libraries
for action in source build
do
    echo "generate ${action}"
    $workspace/client/hsnmailenbeheer/generate.py $action
    rc=$?
    if [ $rc -ne 0 ] ; then
        echo -e "Unable to install javascript libraries ${workspace}/client/hsnmailenbeheer/generate.py ${action}"
        exit 1
    fi
done


# Collect the static files
python $workspace/server/manage.py collectstatic --noinput


# Test
python $workspace/server/manage.py test $workspace/server
rc=$?
if [ $rc -eq 0 ] ; then
    # ToDo: parse the test report
    mkdir -p "target/test-reports"
else
    echo -e "There are test failures."
    exit $rc
fi


# Create the artifact
mkdir -p target
build=target/$instance-$version.tar.gz
tar -pczf $build $workspace


# clean up
deactivate
rm -rf $workspace/*


if [ -f $build ] ; then
    echo "I think we are done for today."
    exit 0
else
    echo -e "Unable to create the artifact."
    exit 1
fi

exit 1