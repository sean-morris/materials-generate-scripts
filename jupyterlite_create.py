import json
import os
import shutil
from util import process_ipynb, strip_unnecessary_keys


def replace_jl_otter_declare(file_path, name):
    inf = "https://www.inferentialthinking.com/data"
    with open(file_path) as f:
        data = json.load(f)
        for cell in data["cells"]:
            imp = cell["source"]
            for index in range(len(imp)):
                if "otter.Notebook" in imp[index]:
                    imp[index] = f"grader = otter.Notebook(\"{name}\", jupyterlite=True)"

                if inf in imp[index]:
                    imp[index] = imp[index].replace(inf, "https://ds-modules.github.io/materials-sp22-assets")

        json_object = json.dumps(data, indent=1)
        with open(file_path, "w") as outfile:
            outfile.write(json_object)


def jupyterlite(a_args, local_notebooks_folder):
    root_copy_path = f"{os.getcwd()}/{local_notebooks_folder}_jupyterlite"
    rel_path = f"{a_args['assign_type']}/{a_args['file_no_ext']}"
    file_name = f"{a_args['file_no_ext']}.ipynb"
    copy_to = os.path.join(root_copy_path, rel_path)
    copy_to_file = os.path.join(copy_to, file_name)
    copy_from = f"{local_notebooks_folder}/{a_args['assign_type']}/{a_args['file_no_ext']}/student"

    shutil.copytree(copy_from, copy_to, dirs_exist_ok=True)

    insert_headers = [
        "# The pip install can take a minute\n",
        f"%pip install -q urllib3<2.0 otter-grader=={a_args['otter_version']} datascience ipywidgets\n",
        "import pyodide_http\n",
        "pyodide_http.patch_all()\n"
    ]
    process_ipynb(copy_to_file, insert_headers)
    strip_unnecessary_keys(copy_to_file)
    replace_jl_otter_declare(copy_to_file, file_name)
    print(f"JupyterLite: {copy_to}/ Created")
