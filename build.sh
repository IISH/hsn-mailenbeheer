#!/bin/bash
#
# ./build.sh [instance] [version] [workspace] [python distribution]
#
# Build script for the project to produce a packaged distribution.
#
# Example: ./build.sh hsn-mailenbeheer 1.0.0 /home/hsn-mailenbeheer /usr/share/python/2.7.11
#
# Requirements: virtualenv and pip must be installed with the targeted python distribution.

APPLICATION_NAME="django"


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
    echo "Setting default workspace to ${workspace}"
fi
builddir="${workspace}/${APPLICATION_NAME}"

p=$4
if [ -z "$p" ] ; then
    p=$(which python)
    echo "Setting default python to system ${p}"
fi


revision=$(git rev-parse HEAD)
echo "instance=${instance}"
echo "version=${version}"
echo "workspace=${workspace}"
echo "builddir=${builddir}"
echo "python distribution=${p}"
echo "revision=${revision}"



# Remove any previous builds
if [ -d target ] ; then
    rm -rf target
fi


# Create a workspace
if [ -d $builddir ] ; then
    rm -rf $builddir
fi
rsync -av --progress --exclude='build.sh' --exclude='.git' . $builddir


# Rename the settings file.
mv "${builddir}/server/hsnmailenbeheer/settings_local_sample.py" "${builddir}/server/hsnmailenbeheer/settings_local.py"


# Setup and activate a virtual environment
$p/bin/virtualenv $builddir/virtualenv
. $builddir/virtualenv/bin/activate


# Retrieve the dependencies for python 2.7
pip install -r $builddir/doc/requirements_py2.7.txt --cache-dir=$workspace


# Build the javascript libraries
for action in source build
do
    echo "generate ${action}"
    $builddir/client/hsnmailenbeheer/generate.py $action
    rc=$?
    if [ $rc -ne 0 ] ; then
        echo -e "Unable to install javascript libraries ${builddir}/client/hsnmailenbeheer/generate.py ${action}"
        exit 1
    fi
done


# Collect the static files
python $builddir/server/manage.py collectstatic --noinput
echo $revision > $builddir/static/revision.txt


# Test
python $builddir/server/manage.py test $builddir/server
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
package=target/$instance-$version.tar.gz
tar -pczf $package -C $workspace $APPLICATION_NAME


# clean up
deactivate
rm -rf $builddir

tar tf $package
rc=$?
if [ $rc -eq 0 ] ; then
    echo "I think we are done for today."
    exit 0
else
    echo -e "Unable to create the artifact."
    exit 1
fi

exit 1