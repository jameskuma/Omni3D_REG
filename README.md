# Omni3D_REG

## 声明

* 所有.sh中均存在`source miniconda3/bin/activate camerabooth`激活conda环境的语句, 使用前请替换
* 所有.sh .py文件中存在使用绝对路径的问题，使用前请核对更换, 建议在vscode中`Ctrl+Shift+F`输入`gaozelin`替换自己的路径

## 第一步 批量复制文件到OO3D目录下

运行`python run_save_path.py`

会自动创建三种txt文件到当前目录下
* OO3D_PATH.txt: 存放 源IMAGE&MASK 地址, 例如 /mnt/petrelfs/share_data/wutong/DATA/OO3D/Align/only_standard/anise/anise_001
* OO3D_NAME.txt: 存放 class 名称, 例如 anise_001
* OO3D_MODEL_PATH.txt: 存放 OBJ 地址, 例如 /mnt/petrelfs/share_data/wutong/DATA/OO3D/data_scans/Align/anise/anise_001

运行`sh run_batch_cpoysh`

会自动创建OO3D文件夹, 所有文件会copy到里面

## 第二步 批量Mask图像

运行`sh run_batch_filter.sh`

* 这里批量Mask还是会存在问题
* 修改Mask方法, 在`run_img_filter.py line44`

## 第三步 批量COLMAP

使用前请下载COLMAP对应的容器文件 (保存在我的google drive 不方便下载可以直接联系我)

`wget https://docs.google.com/uc?export=download&id=${GOODLEID}&confirm=yes -O colmap_ok.sif --no-check-certificate`

运行`sh run_batch_colmap.sh`

* 调整COLMAP内部参数, 请在`run_sfm.sh`文件中修改，注意调整前记得备份 (这版参数是我跳出来效果最好的了2333)
* 调整并行SFM数量, 请在`run_sfm.py`文件中修改`max_thread`参数即可
* 因为COLMAP会产生较大的cache, 因此时不时可以运行`python run_clean_cahe.py`

## 第四步 批量Registration & Save

使用前请下载Open3d对应的容器文件 (保存在我的google drive 不方便下载可以直接联系我)

`wget https://docs.google.com/uc?export=download&id=${GOODLEID}&confirm=yes -O open3d_latest.sif --no-check-certificate`

运行`sh run_batch_reg.sh`

* 结果保存在对应class文件夹中的transformation.json, 例如 OO3D/anise_002/transforms.json
* 调整registration参数在reg_program文件夹中的go_match.py文件夹中 (这版参数也是目前效果比较好的, 在批量跑之前有测试过)
