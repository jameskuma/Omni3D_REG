import os

if __name__ == "__main__":
    src_path = "/mnt/petrelfs/share_data/wutong/DATA/OO3D/Align/only_standard"
    src_model_path = "/mnt/petrelfs/share_data/wutong/DATA/OO3D/data_scans/Align"
    ALL_PATH = []
    ALL_NAME = []
    ALL_MODEL_PATH = []
    OO3D_PATH = []
    OO3D_NAME = []
    OO3D_MODEL_PATH = []

    for si in sorted(os.listdir(src_path)):
        if si.endswith(".sh") or si.endswith("duo") or si.endswith(".p_tar.sh.swp"):
            pass
        else:
            spathi = f"{src_path}/{si}"
            ALL_PATH.append(f"{spathi}")
            ALL_NAME.append(f"{si}")

    for si in sorted(os.listdir(src_model_path)):
        if si in ALL_NAME:
            spathi = f"{src_model_path}/{si}"
            ALL_MODEL_PATH.append(f"{spathi}")

    prec_init = 0.295
    prec_final = 0.300
    ALL_PATH = ALL_PATH[int(prec_init * len(ALL_PATH)):int(prec_final * len(ALL_PATH))]
    ALL_NAME = ALL_NAME[int(prec_init * len(ALL_NAME)):int(prec_final * len(ALL_NAME))]
    ALL_MODEL_PATH = ALL_MODEL_PATH[int(prec_init * len(ALL_MODEL_PATH)):int(prec_final * len(ALL_MODEL_PATH))]

    for pi in ALL_PATH:
        for clsi in sorted(os.listdir(pi)):
            pathi = f"{pi}/{clsi}"
            OO3D_PATH.append(f"{pathi}")
            OO3D_NAME.append(f"{clsi}")

    for pi in ALL_MODEL_PATH:
        for clsi in sorted(os.listdir(pi)):
            if clsi in OO3D_NAME:
                pathi = f"{pi}/{clsi}"
                OO3D_MODEL_PATH.append(f"{pathi}")

    os.makedirs(f"OO3D", exist_ok=True)

    with open("OO3D/OO3D_PATH.txt", "w") as f:
        for PI in OO3D_PATH:
            f.write(f"{PI}\n")

    with open("OO3D/OO3D_NAME.txt", "w") as f:
        for NI in OO3D_NAME:
            f.write(f"{NI}\n")

    with open("OO3D/OO3D_MODEL_PATH.txt", "w") as f:
        for MPI in OO3D_MODEL_PATH:
            f.write(f"{MPI}\n")   