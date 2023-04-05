import os
import json

PARENT_PATH=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
ORIGINAL_MATERIALS_REPO="materials-sp22"
ORIGINAL_MATERIALS_REPO_PATH=f"{PARENT_PATH}/{ORIGINAL_MATERIALS_REPO}"
COLAB_COPY_PATH=f"{PARENT_PATH}/{ORIGINAL_MATERIALS_REPO}-colab"
BINDER_COPY_PATH=f"{PARENT_PATH}/{ORIGINAL_MATERIALS_REPO}-binder"
JUPYTERLITE_COPY_PATH=f"{PARENT_PATH}/{ORIGINAL_MATERIALS_REPO}-jl"

for root, dirs, files in os.walk(ORIGINAL_MATERIALS_REPO_PATH, topdown=False):
    for name in files:
        if ".ipynb" in name:
            file_path=os.path.join(root, name)
            with open(file_path) as f:
                data = json.load(f)
                imp = data["cells"][0]["source"]
                if "otter" in "".join(imp):
                    imp.insert(0, "%pip install otter-grader\n")
                    imp.insert(1, "%pip install datascience\n")
                    print(imp)
                    # Serializing json
                    json_object = json.dumps(data, indent=1)
                
                    #Writing to sample.json
                    with open(name, "w") as outfile:
                        outfile.write(json_object)
            break
    break
