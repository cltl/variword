#!/bin/bash

VOC=$1
OUT=$2
SIZE=$3

./word2vecf/create_init -wvocab $VOC -cvocab $VOC -output $OUT -size ${SIZE}

