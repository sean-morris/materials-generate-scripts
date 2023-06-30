import os
import shutil

copy_from = f"{os.getcwd()}/notebooks_no_footprint_colab"
parent = "/".join(os.getcwd().split("/")[:-1])
for root, dirs, files in os.walk(copy_from):
    for file in files:
        if "student" in root and "tests" not in root:
            file_path = os.path.join(root, file)
            rel_path = "/".join(file_path.split("/")[7:-2])
            copy_from = "/".join(file_path.split("/")[:-1])
            copy_to = f"{parent}/materials-sp22-colab-no-footprint/{rel_path}"
            shutil.copytree(copy_from, copy_to)
