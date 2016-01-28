#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR=$(dirname "$DIR")
LIBS=$DIR/libs

cd $DIR
mkdir -p $LIBS
PIP_REQUIRE_VIRTUALENV=false pip install -r $BASE_DIR/requirements.txt --install-option="--prefix=$LIBS"

# add source files to zip
mkdir -p $BASE_DIR/dist
rm $BASE_DIR/dist/breda.zip || true
pushd $BASE_DIR
zip -r $BASE_DIR/dist/breda.zip * -x "*.git*" -x "*dist*" -x "*scripts*"
popd

# add dependencies to zip
pushd "$LIBS/lib/python2.7/site-packages/"
zip -r $BASE_DIR/dist/breda.zip *
popd
