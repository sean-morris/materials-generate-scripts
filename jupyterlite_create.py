import json
import os
import shutil
import argparse
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


def jupyterlite(notebooks_assign, otter_version, is_test):
    root_copy_path = f"{os.getcwd()}/{notebooks_assign}_jupyterlite"
    root_notebooks_assign = f"{os.getcwd()}/{notebooks_assign}"
    for root, dirs, files in os.walk(root_notebooks_assign):
        for file in files:
            if (not is_test and file.endswith(".ipynb")) or (is_test and file == "hw01.ipynb"):
                file_path = os.path.join(root, file)
                is_user_notebook = "student" in file_path or "autograder" in file_path
                if is_user_notebook:
                    rel_path = "/".join(file_path.split("/")[7:-1])
                    copy_from = "/".join(file_path.split("/")[:-1])
                    copy_to = os.path.join(root_copy_path, rel_path)
                    copy_to_file = os.path.join(copy_to, file)
                    shutil.copytree(copy_from, copy_to)
                    shutil.copyfile(file_path, copy_to_file)
                    insert_headers = [
                        "# The pip install can take a minute\n",
                        f"%pip install -q urllib3<2.0 otter-grader=={otter_version} datascience ipywidgets\n",
                        "import pyodide_http\n",
                        "pyodide_http.patch_all()\n"
                    ]
                    process_ipynb(copy_to_file, insert_headers)
                    strip_unnecessary_keys(copy_to_file)
                    replace_jl_otter_declare(copy_to_file, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create jupyterlite notebooks')
    parser.add_argument('local_notebooks_folder', metavar='p', type=str, help='notebooks')
    parser.add_argument('otter_version', metavar='p', type=str, help='4.3.4')
    parser.add_argument('--is_test', metavar='it', type=bool, help='if testing do one notebook', default=False, action=argparse.BooleanOptionalAction)
    args, unknown = parser.parse_known_args()
    folder = f"{args.local_notebooks_folder}_jupyterlite"
    end_path = f"{os.getcwd()}/{folder}/"
    if os.path.exists(end_path):
        shutil.rmtree(end_path)
    jupyterlite(args.local_notebooks_folder, args.otter_version, args.is_test)
    print(f"JupyterLite: {args.local_notebooks_folder} Created")
