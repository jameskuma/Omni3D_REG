# Omni3D Guidance

## Download repo

```
git clone https://github.com/jameskuma/Omni3D_REG.git
```

## How to use
1. Download COLMAP Dock Images

```
cd Omni3D_REG
mkdir -p container && cd container
apptainer pull dock://graffitytech/colmap:3.7-cuda10.2-devel-ubuntu18.04
rename colmap:3.7-cuda10.2-devel-ubuntu18.04.sif colmap_dev.sif
```

2. Preprocess Data

```
cd Omni3D_REG
python python/run_generate_path.py
python python/run_copy.py
python python/filter.py
```

3. Go Dense Reconsrtuction

```
cd Omni3D_REG
sh scripts/run_sfm.sh 8 64 input_you_group_nodelist
```

## Some tools
1. Clean All Results

```
cd Omni3D_REG
python python/run_clean_all.py.sh
```