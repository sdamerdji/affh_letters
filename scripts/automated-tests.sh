#!/bin/sh

# Mock environment variables for unit tests
export XYZ=”dummy”
export XYZ_HOST=”localhost”

# run unit tests in virtualenv
nosetests -v 

if [ $? -ne 0 ]; then
 echo “unit tests failed”
 exit 1
fi
