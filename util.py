import os
import json
import shutil
import nbformat


def get_path_to_notebook(note):
    path = []
    if "hw" in note:
        path.append("hw")
    elif "lab" in note:
        path.append("lab")
    elif "project" in note:
        path.append("project")
    elif "reference" in note:
        path.append("reference")
    path.append(note[0:-6])
    return path


def remove_otter_assign_output(dir_path):
    # remove extra files from tests
    otter_config_path = f"{dir_path}/autograder/otter_config.json"
    otter_log_path = f"{dir_path}/autograder/.OTTER_LOG"
    if os.path.exists(otter_config_path):
        os.remove(otter_config_path)
    if os.path.exists(otter_log_path):
        os.remove(otter_log_path)


def remove_key(d, key):
    if isinstance(d, dict):
        if key in d:
            del d[key]
        for v in d.values():
            remove_key(v, key)
    elif isinstance(d, list):
        for v in d:
            remove_key(v, key)


def strip_unnecessary_keys(file_name):
    with open(file_name, 'r') as f:
        data_id = json.load(f)
        remove_key(data_id, "execution")
        remove_key(data_id, "widgets")
        remove_key(data_id, "model_id")

    os.remove(file_name)
    with open(file_name, 'w') as f:
        json.dump(data_id, f, indent=1)


# this finds the "code" cell closest to the top of the notebook
# if there are no code cells, it inserts one at the top of the
# notebook and returns it
def find_top(data):
    if data["cells"][0]["cell_type"] == "code":
        return data["cells"][0]["source"]
    empty_cell = {
        "cell_type": "code",
        "execution_count": 0,
        "metadata": {},
        "outputs": [],
        "source": [
        ]
    }
    data["cells"].insert(0, empty_cell)
    return data["cells"][0]["source"]


# creates the file path to a local typed directory(binder, colab, jl)
# and returns the new created path
def create_file_path(root, type):
    dir = "/".join(root.split("/")[5:])
    dir = f"{os.getcwd()}/{type}/{dir}"
    os.makedirs(dir, exist_ok=True)
    return dir


def setup_assign_dir(a_args, assign_dir):
    shutil.rmtree(assign_dir, ignore_errors=True)
    os.makedirs(assign_dir, exist_ok=True)
    if "no_footprint" not in assign_dir:
        shutil.copytree(a_args["notebooks_source"], assign_dir, dirs_exist_ok=True)
    else:
        source = f"{a_args['notebooks_source']}/{a_args['file_no_ext']}.ipynb"
        os.makedirs(assign_dir, exist_ok=True)
        shutil.copy(source, assign_dir)


def process_ipynb(file_path, insert_headers):
    with open(file_path) as f:
        data = json.load(f)
        top = find_top(data)
        inserted = False
        for cell in data["cells"]:
            imp = cell["source"]
            str_imp = "".join(imp)
            if not inserted and ("otter" in str_imp or "datascience" in str_imp):
                top.insert(0, "\n")
                for index, pip in enumerate(insert_headers):
                    top.insert(index, pip)
                inserted = True
                # Serializing json
                json_object = json.dumps(data, indent=1)
                with open(file_path, "w") as outfile:
                    outfile.write(json_object)


def add_sequential_ids_to_notebook(notebook_path, file_name_no_ext):
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Iterate over the cells and add a sequential ID if it doesn't have one
    id_counter = 0
    for cell in nb.cells:
        cell['id'] = f"cell-{file_name_no_ext}-{id_counter}"
        id_counter += 1

    # Save the notebook with the new IDs
    with open(f"{notebook_path}", 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)


def colab_first_cell(args, root_path, file, header_file, local_notebooks_folder):
    data_8_repo_url = args["data_8_repo_url"]
    materials_repo = args["colab_materials_repo"]
    if local_notebooks_folder == "notebooks_no_footprint":
        materials_repo = f"{materials_repo}-no-footprint"

    file_path = os.path.join(root_path, file)
    rel_path = "/".join(file_path.split("/")[7:-2])
    if "lectures" in file_path:
        rel_path = "lectures"
    insert_headers = []
    clone_repo_path = f"{data_8_repo_url}/{materials_repo}"
    notebook_path = f"{materials_repo}/{rel_path}"

    with open(header_file, "r") as f:
        for line in f:
            line = line.replace("||CLONE_REPO_PATH||", clone_repo_path)
            line = line.replace("||ORIGINAL_MATERIALS_REPO||", f"{materials_repo}")
            line = line.replace("||NOTEBOOK_DIR||", notebook_path)
            insert_headers.append(line)
    process_ipynb(file_path, insert_headers)
