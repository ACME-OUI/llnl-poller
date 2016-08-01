#!/bin/bash
echo "Starting diagnostic run"
echo $1
source activate uvcdat
metadiags $1
