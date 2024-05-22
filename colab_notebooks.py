import os
import json
import shutil
from subprocess import run
from util import process_ipynb, remove_otter_assign_output, strip_unnecessary_keys
import argparse


def change_colab_assignment_config(root_path, file):
    data = ""
    file_path = os.path.join(root_path, file)
    with open(file_path, "r") as f:
        data = json.load(f)
    top = data["cells"][0]["source"]
    top[-1] = top[-1] + "\n"
    top.append("runs_on: colab\n")
    top.append("tests:\n")
    top.append("    files: true")
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, indent=1)
    return file_path


def assign(root_path, file, pdfs, footprint, run_otter_tests):
    file_path = os.path.join(root_path, file)
    assign_args = ["otter", "assign", "-v"]
    if not pdfs:
        assign_args.append("--no-pdfs")
    if not run_otter_tests:
        assign_args.append("--no-run-tests")
    assign_args.append(file_path)
    assign_args.append(root_path)

    otter_assign_out = run(assign_args, capture_output=True)
    out = (otter_assign_out.stdout).decode("utf-8")
    err = (otter_assign_out.stderr).decode("utf-8")
    
    msg = "All autograder tests passed"
    if not run_otter_tests:
        print(f"Colab {footprint}: Complete: Tests NOT Run: {file}")
    elif msg in out or msg in err:
        print(f"Colab {footprint}: Tests Passed: {file}")
    else:
        print(f"Colab {footprint}: Tests NOT Passed: {file}")
        with open(f"{os.getcwd()}/colab_assign_log_{file}.txt", "a") as f:
            f.write(err)


def create_colab_raw_dir(root, new_file_path):
    os.makedirs(new_file_path, exist_ok=True)
    shutil.copytree(root, new_file_path, dirs_exist_ok=True)


def colab_first_cell(root_path, file, header_file, args):
    otter_version = args.otter_version
    data_8_repo_url = args.data_8_repo_url
    materials_repo = args.materials_repo
    if args.local_notebooks_folder == "notebooks_no_footprint":
        materials_repo = f"{materials_repo}-no-footprint"

    file_path = os.path.join(root_path, file)
    rel_path = "/".join(file_path.split("/")[7:-2])
    if "lectures" in file_path:
        rel_path = "/".join(file_path.split("/")[7:-1])
    insert_headers = []
    clone_repo_path = f"{data_8_repo_url}/{materials_repo}"
    notebook_path = f"{materials_repo}/{rel_path}"

    with open(header_file, "r") as f:
        for line in f:
            line = line.replace("||OTTER_GRADER_VERSION||", otter_version)
            line = line.replace("||CLONE_REPO_PATH||", clone_repo_path)
            line = line.replace("||ORIGINAL_MATERIALS_REPO||", f"{materials_repo}")
            line = line.replace("||NOTEBOOK_DIR||", notebook_path)
            insert_headers.append(line)
    process_ipynb(file_path, insert_headers)


def convert_raw_to_colab_raw(args, is_test, run_otter_tests, test_notebook):
    parent_path = args.local_notebooks_folder
    for folder in ["hw", "lab", "project", "reference"]:
        for root, dirs, files in os.walk(f"{os.getcwd()}/{parent_path}/{folder}"):
            for file in files:
                if (not is_test and file.endswith(".ipynb")) or (is_test and file == test_notebook):
                    new_file_path = root.replace(parent_path, args.output_folder)
                    create_colab_raw_dir(root, new_file_path)
                    change_colab_assignment_config(new_file_path, file)  # adds runs_on
                    assign(new_file_path, file, args.create_pdfs, args.local_notebooks_folder, run_otter_tests)
                    colab_first_cell(f"{new_file_path}/student", file, "colab-header.txt", args)
                    colab_first_cell(f"{new_file_path}/autograder", file, "colab-header.txt", args)
                    remove_otter_assign_output(new_file_path)
                    strip_unnecessary_keys(f"{new_file_path}/student/{file}")

    for root, dirs, files in os.walk(f"{os.getcwd()}/{parent_path}/lectures"):
        new_file_path = root.replace(parent_path, args.output_folder)
        create_colab_raw_dir(root, new_file_path)
        for file in files:    
            if (not is_test and file.endswith(".ipynb")) or (is_test and file == test_notebook and "lec" in test_notebook):
                colab_first_cell(new_file_path, file, "colab-header-lectures.txt", args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Modify notebooks -- removing files and changing paths to file')
    parser.add_argument('local_notebooks_folder', metavar='p', type=str, help='notebooks or notebooks_no_footprint')
    parser.add_argument('--create_pdfs', metavar='cp', type=bool, help='are we creating PDFS', default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument('otter_version', metavar='p', type=str, help='4.4.1')
    parser.add_argument('data_8_repo_url', metavar='p', type=str, help='https://github.com/data-8')
    parser.add_argument('materials_repo', metavar='p', type=str, help='materials-sp22-colab')
    parser.add_argument('--is_test', metavar='it', type=bool, help='if testing do one notebook', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--run_otter_tests', metavar='ot', type=bool, help='This means when otter assign is executed we double check the tests pass', default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument('test_notebook', metavar='p', type=str, help='hw03.ipynb')
    args, unknown = parser.parse_known_args()
    output_folder = f"{args.local_notebooks_folder}_colab"
    end_path = f"{os.getcwd()}/{output_folder}/"
    if os.path.exists(end_path):
        shutil.rmtree(end_path)
    args.output_folder = output_folder
    convert_raw_to_colab_raw(args, args.is_test, args.run_otter_tests, args.test_notebook)
