import os
import numpy as np
from reg_program.reg_helper.registration import PCD_Registration_System
from reg_program.reg_helper.utils.pose_utils import gen_poses

def resave_poses_bds(basedir, T_c2b=None, scale=None):
    poses_bounds = np.load(os.path.join(basedir, 'poses_bounds.npy'))

    poses_hwf = poses_bounds[:, :15].reshape(-1, 3, 5)
    poses = poses_hwf[..., :4]
    hwf = poses_hwf[..., 4:]

    poses = np.concatenate([poses, np.array([0.,0.,0.,1.])[None,None,...].repeat(len(poses),0)], axis=1)
    poses_b_homo = T_c2b[None, ...] @ poses
    poses_b = poses_b_homo[..., :3, :]
    poses_hwf_b = np.concatenate([
        poses_b,
        hwf,
    ], axis=-1)

    poses_bounds[:, :15] = poses_hwf_b.reshape(-1, 15)
    poses_bounds[:, -2:] = poses_bounds[:, -2:] * scale
    np.save(os.path.join(basedir, 'poses_bounds_blender.npy'), poses_bounds)

def go_match(basedir, voxel_size=0.05, sigma=0.5):
    
    pcd_sys = PCD_Registration_System()

    pcd_sys.load_pcd_source_and_target(basedir, N_source=10000, nb_neighbors=10, std_ratio=0.5)
    pcd_sys.preprocess_pcd(voxel_size)

    while True:
        try_num = 0
        try: 
            pcd_sys.start_registration(voxel_size=voxel_size, sigma=sigma)
            T_c2b = np.linalg.inv(pcd_sys.result_fine.transformation)
            break
        except:
            print("Registration fails, system try again.")
            try_num += 1
            if try_num > 3:
                raise RuntimeError("Registration completely fails.")

    pcd_sys.recover_pcd_norm()
    T_b2c = pcd_sys.compute_transformation()
    T_c2b = np.linalg.inv(T_b2c)
    identity_scale_c2b = T_c2b @ T_c2b.T
    scale_c2b = np.sqrt(identity_scale_c2b[0,0])

    # gen_poses(basedir)
    # resave_poses_bds(basedir, T_c2b, scale_c2b)

    pcd_sys.save_pcd(basedir, T_c2b)
    return T_c2b