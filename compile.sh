#! /bin/bash

CPYTHON="/usr/include/python3.4m"
CPYTHON_OPTS=('-lpython3.4m' '-lpthread' '-lm' '-lutil' '-ldl')

PYTHON_SCRIPT=$1
TARGET_BIN=$2
shift 2


echo "Compiling: ${PYTHON_SCRIPT}"

if [ "$(file -bi ${PYTHON_SCRIPT})" == "text/x-python; charset=us-ascii" ]; then
	TMP=$(mktemp --suffix=".c")
	cython3 -3 --embed -o ${TMP} ${PYTHON_SCRIPT}
	gcc -Os -I ${CPYTHON} -o ${TARGET_BIN} ${TMP} ${CPYTHON_OPTS[@]}
	rm ${TMP}
else
	echo "Not a python script: ${PYTHON_SCRIPT}" 1>&2
	exit 1
fi
