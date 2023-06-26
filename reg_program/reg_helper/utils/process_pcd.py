import open3d as o3d

def pcd_filter_static(pcd, nb_neighbors=20, std_ratio=1.0):
    _, ind = pcd.remove_statistical_outlier(nb_neighbors, std_ratio)
    pcd = pcd.select_by_index(ind)
    return pcd

def preprocess_point_cloud(pcd, voxel_size, log=False):
    if log:
        print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    if log:
        print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    if log:
        print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh

def read_pcd(path):
    pcd = o3d.io.read_point_cloud(path)
    return pcd

def read_mesh_as_pcd(path, N_samples=10000):
    mesh = o3d.io.read_triangle_mesh(path)
    mesh.compute_vertex_normals()
    pcd = mesh.sample_points_poisson_disk(N_samples)
    return pcd