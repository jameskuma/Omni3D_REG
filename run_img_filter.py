import os
import tqdm
import imageio
import numpy as np

def get_configs():
    import configargparse

    parser = configargparse.ArgumentParser()
    parser.add_argument('--li', type=str)
    return parser.parse_args()

def to8b(img):
    return (np.clip(img, 0., 1.)*255.).astype(np.uint8)

if __name__ == "__main__":

    args = get_configs()

    fi = f"OO3D/{args.li}"
    image_fpi = f"{fi}/images"
    matting_fpi = f"{fi}/matting"
    masking_fpi = f"{fi}/masks"
    if not os.path.exists(masking_fpi):
        os.makedirs(masking_fpi)

    image_list = sorted(os.listdir(image_fpi))
    matting_list = sorted(os.listdir(matting_fpi))
    for i in tqdm.tqdm(range(len(image_list)), leave=False):
        imgi = np.array(imageio.imread(f"{image_fpi}/{image_list[i]}"))/255.
        mati = np.array(imageio.imread(f"{matting_fpi}/{matting_list[i]}"))/255.

        if imgi.shape[0] > imgi.shape[1]:
            imgi = np.transpose(imgi, (1,0,2))
        if mati.shape[0] > mati.shape[1]:
            if len(mati.shape) == 3:
                mati = np.transpose(mati, (1,0,2))
            else:
                mati = np.transpose(mati, (1,0))
        if len(mati.shape) == 2:
            mati = mati[..., None]

        # * add alpha into image
        imgi = imgi*mati + (1. - mati)

        imageio.imwrite(f"{image_fpi}/{image_list[i]}", to8b(imgi))