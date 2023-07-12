import os
import json
import shutil
from subprocess import run
from util import process_ipynb, remove_otter_assign_output
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


def assign(root_path, file, pdfs, footprint):
    file_path = os.path.join(root_path, file)
    if pdfs:
        assign_args = ["otter", "assign", "-v", file_path, root_path]
    else:
        assign_args = ["otter", "assign", "-v", "--no-pdfs", file_path, root_path]
    otter_assign_out = run(assign_args, capture_output=True)
    out = (otter_assign_out.stdout).decode("utf-8")
    err = (otter_assign_out.stderr).decode("utf-8")
    msg = "All autograder tests passed"
    if msg in out or msg in err:
        print(f"Colab {footprint}: Tests Passed: {file}")
    else:
        print(f"Colab {footprint}: Tests NOT Passed: {file}")
        print(err)


def create_colab_raw_dir(root, new_file_path):
    os.makedirs(new_file_path, exist_ok=True)
    shutil.copytree(root, new_file_path, dirs_exist_ok=True)


def colab_first_cell(root_path, file, args):
    otter_version = args.otter_version
    data_8_repo_url = args.data_8_repo_url
    materials_repo = args.materials_repo
    if args.local_notebooks_folder == "notebooks_no_footprint":
        materials_repo = f"{materials_repo}-no-footprint"

    file_path = os.path.join(root_path, file)
    rel_path = "/".join(file_path.split("/")[7:-2])
    insert_headers = []
    clone_repo_path = f"{data_8_repo_url}/{materials_repo}"
    notebook_path = f"{materials_repo}/{rel_path}"

    with open("colab-header.txt", "r") as f:
        for line in f:
            line = line.replace("||OTTER_GRADER_VERSION||", otter_version)
            line = line.replace("||CLONE_REPO_PATH||", clone_repo_path)
            line = line.replace("||ORIGINAL_MATERIALS_REPO||", f"{materials_repo}")
            line = line.replace("||NOTEBOOK_DIR||", notebook_path)
            insert_headers.append(line)
    process_ipynb(file_path, insert_headers)


def convert_raw_to_colab_raw(args, is_test):
    parent_path = args.local_notebooks_folder
    for folder in ["hw", "lab", "lectures", "project", "reference"]:
        for root, dirs, files in os.walk(f"{os.getcwd()}/{parent_path}/{folder}"):
            for file in files:
                if (not is_test and file.endswith(".ipynb")) or (is_test and file == "hw01.ipynb"):
                    new_file_path = root.replace(parent_path, args.output_folder)
                    create_colab_raw_dir(root, new_file_path)
                    change_colab_assignment_config(new_file_path, file)  # adds runs_on
                    assign(new_file_path, file, args.pdfs, args.local_notebooks_folder)
                    colab_first_cell(f"{new_file_path}/student", file, args)
                    colab_first_cell(f"{new_file_path}/autograder", file, args)
                    remove_otter_assign_output(new_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Modify notebooks -- removing files and changing paths to file')
    parser.add_argument('local_notebooks_folder', metavar='p', type=str, help='notebooks or notebooks_no_footprint')
    parser.add_argument('otter_version', metavar='p', type=str, help='4.3.4')
    parser.add_argument('data_8_repo_url', metavar='p', type=str, help='https://github.com/data-8')
    parser.add_argument('materials_repo', metavar='p', type=str, help='materials-sp22-colab')
    parser.add_argument('--is_test', metavar='it', type=bool, help='if testing do one notebook', default=False, action=argparse.BooleanOptionalAction)
    args, unknown = parser.parse_known_args()
    output_folder = f"{args.local_notebooks_folder}_colab"
    student_path = f"{os.getcwd()}/notebooks_colab_footprint_student"
    instructor_path = f"{os.getcwd()}/notebooks_colab_footprint_instructor"
    args.pdfs = True
    if "no_footprint" in args.local_notebooks_folder:
        student_path = f"{os.getcwd()}/notebooks_colab_no_footprint_student"
        instructor_path = f"{os.getcwd()}/notebooks_colab_no_footprint_instructor"
        args.pdfs = False
    end_path = f"{os.getcwd()}/{output_folder}/"
    if os.path.exists(end_path):
        shutil.rmtree(end_path)
    if os.path.exists(student_path):
        shutil.rmtree(student_path)
    if os.path.exists(instructor_path):
        shutil.rmtree(instructor_path)
    args.student_path = student_path
    args.instructor_path = instructor_path
    args.output_folder = output_folder
    convert_raw_to_colab_raw(args, args.is_test)
