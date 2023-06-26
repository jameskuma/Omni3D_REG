# coding=UTF-8
import os
import threading

def run_copy(fi, ii, oi):
    cmd = "bash run_copy.sh {} {} {}".format(str(fi),str(ii), str(oi))
    os.system(cmd)
    # print(cmd)

if __name__ == "__main__":
    max_thread = 50
    threads = []
    with open("./OO3D_NAME.txt", "r") as f:
        filenames = f.read().splitlines()

    with open("./OO3D_PATH.txt", "r") as f:
        src_img_paths = f.read().splitlines()

    with open("./OO3D_MODEL_PATH.txt", "r") as f:
        src_obj_paths = f.read().splitlines()

    for fi,ii,oi in zip(filenames, src_img_paths, src_obj_paths):
        # 每当当前的线程数已经达到了max_thread时，等待前max_thread个线程结束后再继续创建新的线程
        while threading.active_count() > max_thread:
            pass
        thread = threading.Thread(target=run_copy, args=(fi,ii,oi,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()  # 等待所有线程结束

    print("All threads finished.")