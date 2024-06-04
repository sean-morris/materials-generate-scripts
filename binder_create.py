import os
import shutil
from util import process_ipynb, strip_unnecessary_keys


def binderize(a_args, local_notebooks_folder):
    root_copy_path = f"{os.getcwd()}/{local_notebooks_folder}_jupyterlite"
    local_path = f"{local_notebooks_folder}/{a_args['assign_type']}/{a_args['file_no_ext']}"
    assign_path = f"{os.getcwd()}/{local_path}"
    file_name = f"{a_args['file_no_ext']}.ipynb"
    file_path = os.path.join(assign_path, file_name)
    for n in ["student", "autograder"]:
        rel_path = "/".join(file_path.split("/")[7:-1])
        copy_from = "/".join(file_path.split("/")[:-1])
        copy_to = os.path.join(root_copy_path, rel_path)
        copy_to_file = os.path.join(copy_to, file_name)
        shutil.copytree(copy_from, copy_to, dirs_exist_ok=True)
        shutil.copyfile(file_path, copy_to_file)
        insert_headers = [
            "# The pip install can take a minute\n",
            f"%pip install -q otter-grader=={a_args['otter_version']}\n",
            "%pip install -q datascience==0.17.5\n"
        ]
        process_ipynb(copy_to_file, insert_headers)
        strip_unnecessary_keys(copy_to_file)
    print(f"Binder: {local_path} Created")
