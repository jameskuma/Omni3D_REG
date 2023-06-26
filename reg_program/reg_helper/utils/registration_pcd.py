import numpy as np
import open3d as o3d

def pc_norm(pc):
    """ Normlize Point Cloud (reference PointNet)
    """
    centroid = np.mean(pc, axis=0)
    pc = pc - centroid
    pc_length = np.sqrt(np.sum(pc ** 2, axis=1))
    pc_lenght_max = np.max(pc_length)
    pc = pc / pc_lenght_max
    return pc, [centroid, pc_lenght_max]

def pc_norm_inverse(pc, centroid, pc_length):
    """Recover Normlized Point Cloud
    """
    pc = pc * pc_length + centroid
    return pc

def global_registration_ransac(source_down, target_down, source_fpfh, target_fpfh, voxel_size=0.05, log=False):
    
    distance_threshold = voxel_size * 1.5
    if log:
        print(":: RANSAC registration on downsampled point clouds.")
        print("   Since the downsampling voxel size is %.3f," % voxel_size)
        print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, 
        target_down, 
        source_fpfh, 
        target_fpfh, 
        True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(with_scaling=True),
        3, 
        [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], 
        o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    return result

def refine_registration_multiscale(source, target, result_global, voxel_size=0.05):
    voxel_sizes = np.array([voxel_size, voxel_size*0.5, voxel_size*0.25])
    distance_thresholds = voxel_sizes * 1.5
    result_coarse = o3d.pipelines.registration.registration_icp(
        source, target, distance_thresholds[0], result_global.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(with_scaling=True),
        o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=1e-4,
                                                          relative_rmse=1e-4,
                                                          max_iteration=10))
    result_to = o3d.pipelines.registration.registration_icp(
        source, target, distance_thresholds[1], result_coarse.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(with_scaling=True),
        o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=1e-5,
                                                          relative_rmse=1e-5,
                                                          max_iteration=15))
    result_fine = o3d.pipelines.registration.registration_icp(
        source, target, distance_thresholds[2], result_to.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(with_scaling=True),
        o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=1e-6,
                                                          relative_rmse=1e-6,
                                                          max_iteration=20))
    return result_fine

def refine_registration_robust(source, target, result_global, sigma=0.1, voxel_size=0.5):
    distance_threshold = voxel_size * 0.5
    loss = o3d.pipelines.registration.TukeyLoss(k=sigma)
    result = o3d.pipelines.registration.registration_icp(
        source, target, 
        distance_threshold, 
        result_global.transformation, 
        o3d.pipelines.registration.TransformationEstimationPointToPlane(loss))
    return result