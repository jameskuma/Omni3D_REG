#!/usr/bin/env bash

# run feature extractor
colmap feature_extractor \
    --database_path ${HOME}/OO3D/$1/database.db \
    --image_path ${HOME}/OO3D/$1/images \
    --SiftExtraction.max_image_size 2400 \
    --SiftExtraction.estimate_affine_shape 1 \
    --SiftExtraction.use_gpu 1 \
    --ImageReader.single_camera 1 &&
# run matching
colmap exhaustive_matcher \
    --database_path ${HOME}/OO3D/$1/database.db \
    --SiftMatching.guided_matching 1 \
    --SiftMatching.use_gpu 1 &&
# sparse ba
mkdir -p ${HOME}/OO3D/$1/sparse &&
colmap mapper \
    --database_path ${HOME}/OO3D/$1/database.db \
    --image_path ${HOME}/OO3D/$1/images \
    --output_path ${HOME}/OO3D/$1/sparse \
    --Mapper.ba_local_max_num_iterations 30 \
    --Mapper.ba_local_max_refinements 5 \
    --Mapper.ba_global_max_num_iterations 75 &&
colmap bundle_adjuster \
    --input_path ${HOME}/OO3D/$1/sparse/0 \
    --output_path ${HOME}/OO3D/$1/sparse/0 \
    --BundleAdjustment.refine_principal_point 1 &&
# run dense dir generation
mkdir -p ${HOME}/OO3D/$1/dense &&
# run image undistortion
colmap image_undistorter \
    --image_path ${HOME}/OO3D/$1/images \
    --input_path ${HOME}/OO3D/$1/sparse/0 \
    --output_path ${HOME}/OO3D/$1/dense \
    --output_type COLMAP \
    --max_image_size 2400 &&
# run patch stereo matching
colmap patch_match_stereo \
    --workspace_path ${HOME}/OO3D/$1/dense \
    --PatchMatchStereo.max_image_size 2400 &&
# run dense reconstruction
colmap stereo_fusion \
    --workspace_path ${HOME}/OO3D/$1/dense \
    --output_path ${HOME}/OO3D/$1/fused.ply

colmap model_converter \
    --input_path ${HOME}/OO3D/$1/sparse/0 \
    --output_path ${HOME}/OO3D/$1/sparse/0 \
    --output_type TXT 