#!/usr/bin/env bash

cd ${HOME}

source miniconda3/bin/activate camerabooth

IND=1
DEGREE=48
for FI in `cat "${HOME}/OO3D_NAME.txt"`
do
    python run_img_filter.py --li ${FI} &
    [ `expr ${IND} % ${DEGREE}` -eq 0 ] && IND=1 && wait
    let IND+=1
done