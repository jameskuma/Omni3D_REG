#!/usr/bin/env bash

PARTITION=3dobject_aigc
JOB_NAME=oo3d_filter
GPUS=1
GPUS_PER_NODE=${GPUS_PER_NODE:-$GPUS}
CPUS_PER_TASK=${CPUS_PER_TASK:-24}

function run_batch_filter() {
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
         bash run_filter.sh
}

run_batch_filter