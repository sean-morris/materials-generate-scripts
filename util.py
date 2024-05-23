import os
import json


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
        remove_key(data_id, "id")
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
