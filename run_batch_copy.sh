#!/usr/bin/env bash

PARTITION=3dobject_aigc
JOB_NAME=oo3d_filter
GPUS=1
GPUS_PER_NODE=${GPUS_PER_NODE:-$GPUS}
CPUS_PER_TASK=${CPUS_PER_TASK:-24}

echo "----copy report start--------"

function run_batch_copy() {
    srun --partition=${PARTITION} \
         --exclude=SH-IDC1-10-140-1-133 \
         --job-name=${JOB_NAME} \
         --gres=gpu:${GPUS_PER_NODE} \
         --ntasks=1 \
         --ntasks-per-node=1 \
         --mem-per-cpu=100000 \
         --quotatype=auto \
         --cpus-per-task=${CPUS_PER_TASK} \
         --kill-on-bad-exit=0 \
         python run_copy.py
}

cd ${HOME}
if [ ! -d "OO3D" ]; then
  mkdir "OO3D"
fi
source miniconda3/bin/activate camerabooth
run_batch_copy

echo "----copy report end--------"