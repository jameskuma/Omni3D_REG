import tqdm
import numpy as np
import open3d as o3d
from reg_program.reg_helper.utils import process_pcd, registration_pcd

class PCD_Registration_System():
    def __init__(self) -> None:
        print("Blender&COLMAP Point Cloud Registration Tool Copyright (C) 2023-2023 Zelin Gao, Zhejiang Unversity.\n" + \
              "This program is done during his internship in S(hang)H(ai)lab.\n" + \
              "This software is still under test over about 5k+ objects registration, and you are welcome to report any issue!")

    def load_pcd_source_and_target(self, basedir, nb_neighbors, std_ratio, N_source, source_is_ply=False):
        print("1. Load Point Cloud from Source (blender) and Target (colmap).")
        # * load point cloud
        # from colmap (target), remove outliers by static anylsis
        target_path = f"{basedir}/fused.ply"
        pcd_target = process_pcd.read_pcd(target_path)
        pcd_target = process_pcd.pcd_filter_static(pcd_target, nb_neighbors, std_ratio)
        # from blender (source)
        source_path = f"{basedir}/Scan.obj"
        pcd_source = process_pcd.read_mesh_as_pcd(source_path, N_source)
        # * normalize point cloud
        pcd_target_rescale, cen_len_target = registration_pcd.pc_norm(np.asarray(pcd_target.points))
        pcd_target.points = o3d.utility.Vector3dVector(pcd_target_rescale)
        pcd_source_rescale, cen_len_source = registration_pcd.pc_norm(np.asarray(pcd_source.points))
        pcd_source.points = o3d.utility.Vector3dVector(pcd_source_rescale)
        # * define point cloud in class
        self.pcd_source = pcd_source
        self.pcd_target = pcd_target
        self.cen_len_source = cen_len_source
        self.cen_len_target = cen_len_target
        self.pcd_target.paint_uniform_color([1, 0, 0])
        self.pcd_source.paint_uniform_color([0, 0, 1])

    def preprocess_pcd(self, voxel_size=0.05):
        print("2. Preprocess Point Cloud (normals estimation and feature extraction).")
        # * estimate normals and features
        self.pcd_target, self.fpfh_target = process_pcd.preprocess_point_cloud(self.pcd_target, voxel_size=voxel_size)
        self.pcd_source, self.fpfh_source = process_pcd.preprocess_point_cloud(self.pcd_source, voxel_size=voxel_size)

    def start_registration(self, voxel_size=0.05, sigma=0.1):
        print("3. Registration Point Cloud from Coarse to Fine.")
        for i in tqdm.tqdm(range(3), desc="performing registration"):
            if i == 0:
                # * perform global registration (inital transformation)
                result_ransac = registration_pcd.global_registration_ransac(self.pcd_source, 
                                                                            self.pcd_target,
                                                                            self.fpfh_source, 
                                                                            self.fpfh_target,
                                                                            voxel_size)
            elif i == 1:
                # * perform local refinement registration (coarse-to-fine)
                result_coarse = registration_pcd.refine_registration_multiscale(self.pcd_source, 
                                                                                self.pcd_target, 
                                                                                result_ransac, 
                                                                                voxel_size)
            else:
                self.result_fine = registration_pcd.refine_registration_robust(self.pcd_source, 
                                                                               self.pcd_target,
                                                                               result_coarse, 
                                                                               sigma, 
                                                                               voxel_size)
        print("Done.")

    def recover_pcd_norm(self):
        print("4. Recover Normalized Point Cloud.")
        # * inverse scale point cloud with cen_len info
        pcd_source_inv = registration_pcd.pc_norm_inverse(np.asarray(self.pcd_source.points), self.cen_len_source[0], self.cen_len_source[1])
        self.pcd_source.points = o3d.utility.Vector3dVector(pcd_source_inv)
        pcd_target_inv = registration_pcd.pc_norm_inverse(np.asarray(self.pcd_target.points), self.cen_len_target[0], self.cen_len_target[1])
        self.pcd_target.points = o3d.utility.Vector3dVector(pcd_target_inv)

    def compute_transformation(self):
        print("5. Compute Transformation Matrix.")
        # * calculate the transformation for output
        # R_fine = (l2/l1) * R
        transformation_fine = np.eye(4, dtype=np.float32)
        transformation_fine[:3, :3] = (self.cen_len_target[1] / self.cen_len_source[1] + 1e-8) * self.result_fine.transformation[:3, :3]
        # t_fine = l2 * t + c2 - (l2/l1) * c1
        transformation_fine[:3, -1] = self.cen_len_target[1] * self.result_fine.transformation[:3, -1] + self.cen_len_target[0] - (self.cen_len_target[1] / self.cen_len_source[1] + 1e-8) * self.cen_len_source[0]

        return transformation_fine

    def compute_scale(self, transformation):
        identity_scale = transformation @ transformation.T
        scale = np.sqrt(identity_scale[0,0])
        return scale

    def save_pcd(self, path, T_c2b):
        self.pcd_target.transform(T_c2b)
        o3d.io.write_point_cloud(f"{path}/reg_result.ply", self.pcd_target+self.pcd_source )

    def visual_pcd(self, pcd_source, pcd_target, name=None):
        o3d.visualization.draw_geometries([pcd_source, pcd_target], window_name=name)