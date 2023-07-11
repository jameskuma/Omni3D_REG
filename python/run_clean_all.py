import os
import tqdm
import shutil

if __name__ == "__main__":
    paths = [f'OO3D/{i}' for i in sorted(os.listdir("OO3D"))]

    for path in paths:
        if path.endswith('txt'):
            continue
        if os.path.exists(f'{path}/dense'):
            shutil.rmtree(f'{path}/dense')
            shutil.rmtree(f'{path}/sparse')

        if os.path.exists(f'{path}/fused.ply'):
            os.remove(f'{path}/database.db')
            os.remove(f'{path}/fused.ply')
            os.remove(f'{path}/fused.ply.vis')