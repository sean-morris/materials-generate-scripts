import os
import json
import shutil

PARENT_PATH=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
DATA_8_REPO_URL="https://github.com/data-8"
ORIGINAL_MATERIALS_REPO="materials-sp22"
CLONE_REPO_PATH=f"{DATA_8_REPO_URL}/{ORIGINAL_MATERIALS_REPO}"
ORIGINAL_MATERIALS_REPO_PATH=f"{PARENT_PATH}/{ORIGINAL_MATERIALS_REPO}"
OTTER_GRADER_VERSION="4.3.1"


#creates the file path to a local typed directory(binder, colab, jl)
#and returns the new created path
def create_file_path(root, type, name):
    dir = "/".join(root.split("/")[5:])
    dir = f"{os.getcwd()}/{type}/{dir}"
    os.makedirs(dir, exist_ok=True)
    return os.path.join(dir, name)

def process_ipynb(file_path, insert_headers):
    with open(file_path) as f:
        data = json.load(f)
        top = data["cells"][0]["source"]
        inserted = False
        for cell in data["cells"]:
            imp = cell["source"]
            str_imp = "".join(imp)
            if not(inserted) and ("otter" in str_imp or "datascience" in str_imp):
                for index, pip in enumerate(insert_headers):
                    top.insert(index, pip)
                inserted = True
                print(imp)
                # Serializing json
                json_object = json.dumps(data, indent=1)
                with open(file_path, "w") as outfile:
                    outfile.write(json_object)

def binderize(root, name):
    file_path=create_file_path(root, "binder", name)
    shutil.copyfile(f"{root}/{name}",file_path)
    if ".ipynb" in name:
        insert_headers = [
            f"# The pip install can take a minute\n",
            f"%pip install -q otter-grader=={OTTER_GRADER_VERSION}\n",
            "%pip install -q datascience\n"
        ]
        process_ipynb(file_path, insert_headers)

def jupyterlite(root, name):
    file_path=create_file_path(root, "jupyterlite", name)
    shutil.copyfile(f"{root}/{name}",file_path)
    if ".ipynb" in name:
        insert_headers = [
            f"# The pip install can take a minute\n",
            "import micropip\n",
            f"await micropip.install('otter-grader=={OTTER_GRADER_VERSION}')\n",
            "await micropip.install('datascience')\n"
        ]    
        process_ipynb(file_path, insert_headers)

def colab(root, name):
    file_path=create_file_path(root, "colab", name)
    shutil.copyfile(f"{root}/{name}",file_path)
    if ".ipynb" in name:
        insert_headers = []
        with open("colab-header.txt", "r") as f:
            for line in f:
                line = line.replace("||OTTER_GRADER_VERSION||", OTTER_GRADER_VERSION)
                line = line.replace("||CLONE_REPO_PATH||", CLONE_REPO_PATH)
                line = line.replace("||ORIGINAL_MATERIALS_REPO||", ORIGINAL_MATERIALS_REPO)
                line = line.replace("||NOTEBOOK_DIR||", root[root.index(ORIGINAL_MATERIALS_REPO):])
                insert_headers.append(line)    
        process_ipynb(file_path, insert_headers)

# remove directories entirely
for type in ["colab", "jupyterlite", "binder"]:
    shutil.rmtree(type, ignore_errors=True)

for root, dirs, files in os.walk(ORIGINAL_MATERIALS_REPO_PATH, topdown=False):
    for name in files:
        binderize(root, name)
        colab(root, name)
        jupyterlite(root, name)
    break
