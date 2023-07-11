import os
import timeit
import shutil
import multiprocessing

def run_sfm(root_path, gpu_id):

    # run feature extractor
    cmd_one = f"colmap feature_extractor \
                    --database_path {root_path}/database.db \
                    --image_path {root_path}/masked_images \
                    --SiftExtraction.max_image_size 3800 \
                    --SiftExtraction.estimate_affine_shape 1 \
                    --SiftExtraction.use_gpu 1 \
                    --ImageReader.single_camera 1"
    print(cmd_one)
    os.system(cmd_one)

    # run matching
    cmd_two = f'colmap exhaustive_matcher \
                    --database_path {root_path}/database.db \
                    --SiftMatching.guided_matching 1 \
                    --SiftMatching.use_gpu 1'
    os.system(cmd_two)
    # sparse ba
    cmd_three = f'mkdir -p {root_path}/sparse'
    cmd_four = f'colmap mapper \
                    --database_path {root_path}/database.db \
                    --image_path {root_path}/masked_images \
                    --output_path {root_path}/sparse \
                    --Mapper.ba_local_max_num_iterations 30 \
                    --Mapper.ba_local_max_refinements 5 \
                    --Mapper.ba_global_max_num_iterations 75'
    os.system(cmd_three)
    os.system(cmd_four)
    # run dense dir generation
    cmd_five = f'mkdir -p {root_path}/dense'
    os.system(cmd_five)
    # run image undistortion
    cmd_six = f'colmap image_undistorter \
                    --image_path {root_path}/masked_images \
                    --input_path {root_path}/sparse/0 \
                    --output_path {root_path}/dense \
                    --output_type COLMAP \
                    --max_image_size 3800'
    os.system(cmd_six)
    
    # run patch stereo matching
    cmd_seven = f'colmap patch_match_stereo \
                    --workspace_path {root_path}/dense \
                    --PatchMatchStereo.max_image_size 3800'
    os.system(cmd_seven)

    # run dense reconstruction
    cmd_eight = f'colmap stereo_fusion \
                        --workspace_path {root_path}/dense \
                        --output_path {root_path}/fused.ply'
    os.system(cmd_eight)

    cmd_nine = f'colmap model_converter \
                        --input_path {root_path}/sparse/0 \
                        --output_path {root_path}/sparse/0 \
                        --output_type TXT'
    os.system(cmd_nine)
    
    if os.path.exists(f"{root_path}/dense/0/stereo"):
        shutil.rmtree(f"{root_path}/dense/0/stereo")
    if os.path.exists(f"{root_path}/dense/stereo"):
        shutil.rmtree(f"{root_path}/dense/stereo")

if __name__ == '__main__':

    cls_paths = []
    for i in sorted(os.listdir('OO3D')):
        if i.endswith('.txt'):
            continue
        cls_paths.append(f'OO3D/{i}')

    cls_paths = cls_paths[:10]

    max_parallel = 10
    num_launches = len(cls_paths)
    gpu_ids = list(range(8)) * (num_launches // 8) + list(range(num_launches % 8))

    time_init = timeit.default_timer()
    processes = []
    for i, (cls_path,gpu_id) in enumerate(zip(cls_paths,gpu_ids)):
        process = multiprocessing.Process(target=run_sfm, args=(cls_path, gpu_id))
        process.start()
        processes.append(process)
        
        if (i + 1) % max_parallel == 0 or i == num_launches - 1:
            for process in processes:
                process.join()
            processes = []

    time_cost = timeit.default_timer() - time_init
    print(f'Time Consuming: {time_cost:.3f} Seconds!')