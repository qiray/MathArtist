#!/bin/bash

set -e

PYTHON=python

check_python() {
    command -v "$1" >/dev/null 2>&1 && 
    "$1" -c 'import sys; assert sys.version_info >= (3, 0)' 2>/dev/null && 
    echo "$1"
}

get_python() {
    check_python python || check_python python3 || { 
        echo >&2 "I require python 3 but it's not installed. Aborting."
        exit 1
    }
}

build_cython() {
    $PYTHON setup.py build_ext --inplace
}

build_pyinstaller() {
    echo "Building executable"
    ADD_BINARY=""
    if [[ "$OSTYPE" == "linux-gnu" ]]; then
        ADD_BINARY=--add-binary="/usr/lib64/libGL.so.1:lib"
    fi
    pyinstaller --onefile --windowed main.py -n mathartist --hidden-import=palettes $ADD_BINARY --icon=icon.ico
    cp -r data dist/
    cp -r samples dist/
    cp icon.ico dist/
    cp README.md dist/
    cp LICENSE dist/
    mkdir -p dist/output
    echo "Done!"
}

echo "Checking for python 3"
PYTHON=$(get_python)
echo "Found python 3 - $PYTHON"

PREBUILD=false
CYTHON=false
INSTALL=false
CLEAN=false
if [[ $# -eq 0 ]]; then
    PREBUILD=true
    CYTHON=true
fi
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        install)
        INSTALL=true
        shift # pass argument
        ;;
        cython)
        CYTHON=true
        shift
        ;;
        full)
        PREBUILD=true
        CYTHON=true
        INSTALL=true
        shift
        ;;
        prebuild)
        PREBUILD=true
        shift
        ;;
        clean)
        CLEAN=true
        shift
        ;;
        *)
        echo "Unknown argument"
        exit 0
        ;;
    esac
done

$CLEAN && {
    rm -f -- *.c *.so *.pyd
    exit 0
}

$PREBUILD && {
    echo "Installing requirements"
    $PYTHON -m pip install -r requirements.txt --user
}

$CYTHON && {
    build_cython
}

$INSTALL && {
    build_pyinstaller
}
