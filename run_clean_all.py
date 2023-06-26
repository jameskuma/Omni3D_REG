import os
import tqdm
import shutil

if __name__ == "__main__":
    path = sorted(os.listdir("./OO3D"))
    for i in tqdm.tqdm(range(len(path)), desc="cleaning wrong cache"):
        pi = path[i]
        files = sorted(os.listdir(f"./OO3D/{pi}"))
        if "database.db" in files:
            os.remove(f"./OO3D/{pi}/database.db")
        if "database.db-shm" in files:
            os.remove(f"./OO3D/{pi}/database.db-shm")
        if "database.db-wal" in files:
            os.remove(f"./OO3D/{pi}/database.db-wal")
        if "sparse" in files:
            shutil.rmtree(f"./OO3D/{pi}/sparse")
        if "dense" in files:
            shutil.rmtree(f"./OO3D/{pi}/dense")
        if f"{pi}.ply" in files:
            os.remove(f"./OO3D/{pi}/{pi}.ply") 
        if f"{pi}.ply.vis" in files:
            os.remove(f"./OO3D/{pi}/{pi}.ply.vis") 