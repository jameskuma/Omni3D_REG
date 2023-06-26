#!/usr/bin/env bash

# set -x

PARTITION=3dobject_aigc
JOB_NAME=registration
GPUS=1
GPUS_PER_NODE=${GPUS_PER_NODE:-$GPUS}
CPUS_PER_TASK=${CPUS_PER_TASK:-8}

srun --partition=${PARTITION} \
     --exclude=SH-IDC1-10-140-1-133 \
     --nodelist=SH-IDC1-10-140-1-172 \
     --job-name=${JOB_NAME} \
     --gres=gpu:${GPUS_PER_NODE} \
     --ntasks=1 \
     --ntasks-per-node=1 \
     --mem-per-gpu=81251 \
     --quotatype=reserved \
     --cpus-per-task=${CPUS_PER_TASK} \
     --kill-on-bad-exit=0 \
     --pty \
     apptainer exec --nv --bind /mnt:/mnt open3d_latest.sif \
     bash
    #  apptainer pull docker://alansavio25/open3d:latest
     