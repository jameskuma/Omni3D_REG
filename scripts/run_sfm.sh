#!/usr/bin/env bash

PARTITION=3dobject_aigc
JOB_NAME=oo3d_sfm
GPUS=$1
CPUS=$2
NODELINK=$3
GPUS_PER_NODE=${GPUS_PER_NODE:-$GPUS}
CPUS_PER_TASK=${CPUS_PER_TASK:-$CPUS}

echo "----batch colmap report start--------"

source ${HOME}/miniconda3/bin/activate zero123
mkdir -p ${HOME}/Omni_REG
cd ${HOME}/Omni_REG

srun --partition=${PARTITION} \
     --exclude=SH-IDC1-10-140-1-133 \
     --nodelist=${NODELINK} \
     --job-name=${JOB_NAME} \
     --gres=gpu:${GPUS_PER_NODE} \
     --ntasks=1 \
     --ntasks-per-node=1 \
     --quotatype=auto \
     --cpus-per-task=${CPUS_PER_TASK} \
     --kill-on-bad-exit=0 \
     apptainer exec --nv --bind /mnt:/mnt container/colmap_dev.sif \
     python3 python/run_sfm.py

echo "----batch colmap report end--------"