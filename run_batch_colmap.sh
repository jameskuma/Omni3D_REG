#!/usr/bin/env

# set -x

PARTITION=3dobject_aigc
JOB_NAME=oo3d_sfm
GPUS=8
GPUS_PER_NODE=${GPUS_PER_NODE:-$GPUS}
CPUS_PER_TASK=${CPUS_PER_TASK:-80}

function run_batch_colmap() {
    srun --partition=${PARTITION} \
         --exclude=SH-IDC1-10-140-1-133 \
         --job-name=${JOB_NAME} \
         --ntasks=1 \
         --threads=60 \
         --ntasks-per-node=1 \
         --mpi=pmi2 \
         --quotatype=auto \
         --cpus-per-task=${CPUS_PER_TASK} \
         --kill-on-bad-exit=0 \
         --overcommit \
         apptainer exec --nv --bind /mnt:/mnt colmap_ok.sif \
         python run_sfm.py
}

cd ${HOME}
source miniconda3/bin/activate zero123
run_batch_colmap