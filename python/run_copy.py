import os
import threading

def run_copy(fi, ii, oi):
    print(f"Copying {fi} from {ii} and {oi}")
    os.makedirs(f"OO3D/{fi}", exist_ok=True)
    cmd_copy_image = f"cp -r {ii}/standard/images OO3D/{fi}/"
    cmd_copy_matting = f"cp -r {ii}/standard/matting OO3D/{fi}/"
    cmd_copy_obj = f"cp -r {oi}/Scan/Scan.obj OO3D/{fi}/"

    # print(cmd_copy_image)
    # print(cmd_copy_matting)
    # print(cmd_copy_obj)
    os.system(cmd_copy_image)
    os.system(cmd_copy_matting)
    os.system(cmd_copy_obj)

if __name__ == "__main__":
    max_thread = 50
    threads = []
    with open("OO3D/OO3D_NAME.txt", "r") as f:
        filenames = f.read().splitlines()

    with open("OO3D/OO3D_PATH.txt", "r") as f:
        src_img_paths = f.read().splitlines()

    with open("OO3D/OO3D_MODEL_PATH.txt", "r") as f:
        src_obj_paths = f.read().splitlines()

    for fi,ii,oi in zip(filenames, src_img_paths, src_obj_paths):
        while threading.active_count() > max_thread:
            pass
        thread = threading.Thread(target=run_copy, args=(fi,ii,oi))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("All threads finished.")