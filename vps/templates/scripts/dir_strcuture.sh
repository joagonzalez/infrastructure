#!/bin/bash
# dir_strcuture.sh <project_folder>

echo "Build project structure..."

if [ "$1" != "" ]; then
    mkdir -p $1/src/
    touch $1/src/.gitignore
    mkdir -p $1/doc/
    touch $1/doc/.gitignore
    mkdir -p $1/tests/
    touch $1/tests/.gitignore
    touch $1/README.md
    touch $1/.gitignore
else
    echo "Specify project folder..."
fi

