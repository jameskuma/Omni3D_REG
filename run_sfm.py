# coding=UTF-8
import os
import threading

def run_colmap(filename):
    cmd = "bash run_sfm.sh {}".format(str(filename))
    os.system(cmd)
    # print(cmd)

if __name__ == "__main__":
    max_thread = 10
    threads = []
    with open("./OO3D_NAME.txt", "r") as f:
        filenames = f.read().splitlines()

    for fi in filenames:
        # 每当当前的线程数已经达到了max_thread时，等待前max_thread个线程结束后再继续创建新的线程
        while threading.active_count() > max_thread:
            pass
        thread = threading.Thread(target=run_colmap, args=(fi,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()  # 等待所有线程结束

    print("All threads finished.")