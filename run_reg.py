# coding=UTF-8
import os
import threading

def run_colmap(filename):
    all_files = os.listdir(filename)
    if "dense" in all_files and "fused.ply" in all_files and "Scan.obj" in all_files:
        cmd = f"python /mnt/petrelfs/gaozelin/colmap2nerf.py --basedir {str(filename)} --text {str(filename)}/sparse/0 --images {str(filename)}/images --out {str(filename)}/transforms.json"
        os.system(cmd)

if __name__ == "__main__":
    max_thread = 10
    threads = []
    filenames = sorted(os.listdir("/mnt/petrelfs/gaozelin/OO3D"))

    for fi in filenames:
        fi = f"/mnt/petrelfs/gaozelin/OO3D/{fi}"
        # 每当当前的线程数已经达到了max_thread时，等待前max_thread个线程结束后再继续创建新的线程
        while threading.active_count() > max_thread:
            pass
        thread = threading.Thread(target=run_colmap, args=(fi,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()  # 等待所有线程结束

    print("All threads finished.")