import json
import os
import shutil
import argparse
from util import process_ipynb


def binderize(notebooks_assign, otter_version, is_test):
    root_copy_path = f"{os.getcwd()}/{notebooks_assign}_binder"
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
                        f"%pip install -q otter-grader=={otter_version}\n",
                        "%pip install -q datascience\n"
                    ]
                    process_ipynb(file_path, insert_headers)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create binder notebooks')
    parser.add_argument('local_notebooks_folder', metavar='local_notebooks_folder', type=str, help='notebooks_no_footprint')
    parser.add_argument('otter_version', metavar='otter_version', type=str, help='4.3.4')
    parser.add_argument('--is_test', metavar='it', type=bool, help='if testing do one notebook', default=False, action=argparse.BooleanOptionalAction)
    args, unknown = parser.parse_known_args()
    folder = f"{args.local_notebooks_folder}_binder"
    end_path = f"{os.getcwd()}/{folder}/"
    if os.path.exists(end_path):
        shutil.rmtree(end_path)
    binderize(args.local_notebooks_folder, args.otter_version, args.is_test)
