import binder_create as bc
import colab_notebooks as cn
import copy_to_assets as ca
import jupyterlite_create as jc
import otter_assign as oa
import copy_to_repos as cr
import shutil
import os

assignments = {
    #  "hw": range(1, 13),
    #  "lab": range(1, 11),
    #  "project": range(1, 4),
    "lec": [1] + list(range(3, 22)) + list(range(23, 34)) + list(range(35, 40))
}
reference_notebook = "datascience-to-pandas"
VERBOSE = False
OTTER_VERSION = "4.4.1"
COLAB_CLONE_REPO = "https://github.com/data-8"
COLAB_REPO_MATERIALS = "materials-sp22-colab"


def setup(assign_type, file_no_ext):
    """this removes the old files and copies the raw notebooks
    for this file to notebooks

    Args:
        assign_type (str): e.g. hw, lab, etc
        file_no_ext (str): e.g. hw01
    """
    notebooks_path = f"{os.getcwd()}/notebooks/{assign_type}/{file_no_ext}"
    raw_path = f"{os.getcwd()}/_notebooks_raw/{assign_type}/{file_no_ext}"
    shutil.rmtree(notebooks_path, ignore_errors=True)
    shutil.copytree(raw_path, notebooks_path)
    if VERBOSE:
        print(f"Old files deleted, new copies {file_no_ext}")


def run_assign(assign_type, file_no_ext):
    """run the file through the process

    Args:
        file_path (str): file to run
    """
    raw_path = f"{os.getcwd()}/_notebooks_raw/{assign_type}/{file_no_ext}"
    assign_args = {
        "verbose": VERBOSE,
        "notebooks_source": raw_path,
        "assign_type": assign_type,
        "file_no_ext": file_no_ext,
        "create_pdfs": False,
        "run_otter_tests": True,
        "otter_version": OTTER_VERSION,
        "data_8_repo_url": COLAB_CLONE_REPO,
        "colab_materials_repo": COLAB_REPO_MATERIALS,
        "assets_url": 'https://ds-modules.github.io/materials-sp22-assets'
    }
    cn.colab_assign_for_file(assign_args, "notebooks")
    ca.copy_files_assets_repo(assign_args)
    cn.colab_assign_for_file(assign_args, "notebooks_no_footprint")
    oa.assign(assign_args, "notebooks_no_footprint", create_pdfs=False)
    oa.assign(assign_args, "notebooks", create_pdfs=assign_args["create_pdfs"])
    jc.jupyterlite(assign_args, "notebooks")
    jc.jupyterlite(assign_args, "notebooks_no_footprint")
    bc.binderize(assign_args, "notebooks")
    bc.binderize(assign_args, "notebooks_no_footprint")
    cr.copy_assets(assign_type, file_no_ext)


def handle_lectures(assign_type, file_no_ext):
    assign_args = {
        "verbose": VERBOSE,
        "assign_type": assign_type,
        "file_no_ext": file_no_ext,
        "otter_version": OTTER_VERSION,
        "data_8_repo_url": COLAB_CLONE_REPO,
        "colab_materials_repo": COLAB_REPO_MATERIALS,
        "assets_url": 'https://ds-modules.github.io/materials-sp22-assets'
    }
    notebooks_path = f"{os.getcwd()}/notebooks/{assign_type}"
    colab_path = f"{os.getcwd()}/notebooks_lectures_colab/"
    raw_path = f"{os.getcwd()}/_notebooks_raw/{assign_type}/{file_no_ext}.ipynb"
    if os.path.exists(f"{notebooks_path}/{file_no_ext}.ipynb"):
        os.remove(f"{notebooks_path}/{file_no_ext}.ipynb")
    os.makedirs(notebooks_path, exist_ok=True)
    os.makedirs(colab_path, exist_ok=True)
    shutil.copyfile(raw_path, f"{colab_path}/{file_no_ext}.ipynb")
    shutil.copyfile(raw_path, f"{notebooks_path}/{file_no_ext}.ipynb")
    if VERBOSE:
        print(f"Old files deleted, new copies {file_no_ext}")
    cn.colab_handle_lectures(assign_args, "notebooks")


def run(file):
    """runs the process for one file at a time if the
    parameter, file, is passed in then it will only run for
    that file.

    Args:
        file (str): None or the file to run
    """
    for assign_type, assigns in assignments.items():
        for f in assigns:
            file_no_ext = f"{assign_type}{f:02}"
            if assign_type == "project":
                file_no_ext = f"{assign_type}{f}"
            name = f"{file_no_ext}.ipynb"
            if not file or (file == name):
                if assign_type == "lec":
                    handle_lectures(assign_type, file_no_ext)
                else:
                    setup(assign_type, file_no_ext)
                    run_assign(assign_type, file_no_ext)
    # if not file or (file == f"{reference_notebook}.ipynb"):
    #     run_assign("reference", f"{reference_notebook}")
    print("The notebooks are created!")


# full file name: hw02.ipynb
run("")
