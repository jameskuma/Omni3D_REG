import os
import tqdm
import shutil

if __name__ == "__main__":
    path = sorted(os.listdir("./OO3D"))
    for pi in tqdm.tqdm(path, desc="clean cache"):
        files = sorted(os.listdir(f"./OO3D/{pi}"))
        for i in range(len(files)):
            if os.path.exists(f"./OO3D/{pi}/masks"):
                shutil.rmtree(f"./OO3D/{pi}/masks")
            if files[i].endswith(".ply"):
                if files[i+1].endswith(".ply.vis"):
                    if os.path.exists(f"./OO3D/{pi}/dense/0/stereo"):
                        tqdm.tqdm.write(f"remove {pi} cache")
                        shutil.rmtree(f"./OO3D/{pi}/dense/0/stereo")
                    if os.path.exists(f"./OO3D/{pi}/dense/stereo"):
                        tqdm.tqdm.write(f"remove {pi} cache")
                        shutil.rmtree(f"./OO3D/{pi}/dense/stereo")