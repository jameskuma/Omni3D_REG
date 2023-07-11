import os
import tqdm
import imageio
import threading
import numpy as np

def to8b(img):
    return (np.clip(img, 0., 1.)*255.).astype(np.uint8)

def run_filter(cls_path):
    os.makedirs(f'{cls_path}/masked_images', exist_ok=True)
    image_paths = [f'{cls_path}/images/{i}' for i in sorted(os.listdir(f'{cls_path}/images'))]
    matting_paths = [f'{cls_path}/matting/{i}' for i in sorted(os.listdir(f'{cls_path}/matting'))]
    for image_path,matting_path in tqdm.tqdm(zip(image_paths,matting_paths), desc="Masking Images"):
        image = np.array(imageio.imread(image_path))/255.
        matting = np.array(imageio.imread(matting_path))/255.
        if image.shape[0] > image.shape[1]:
            image = np.transpose(image, (1,0,2))
        if len(matting.shape) == 2:
            matting = matting[..., None]
        matting = matting[..., :1]
        if matting.shape[0] > matting.shape[1]:
            matting = np.transpose(matting, (1,0,2))
        image = image*matting + (1.-matting)
        filename = image_path.split('/')[-1]
        imageio.imwrite(f'{cls_path}/masked_images/{filename}', to8b(image))
    
if __name__ == "__main__":
    max_thread = 50
    threads = []
    cls_paths = []
    for i in os.listdir('OO3D'):
        if i.endswith('.txt'):
            continue
        cls_paths.append(f'OO3D/{i}')

    for cls_path in cls_paths:
        while threading.active_count() > max_thread:
            pass
        thread = threading.Thread(target=run_filter, args=(cls_path,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("All threads finished.")