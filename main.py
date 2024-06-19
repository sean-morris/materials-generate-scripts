import binder_create as bc
import colab_notebooks as cn
import copy_to_assets as ca
import jupyterlite_create as jc
import otter_assign as oa
import copy_to_repos as cr
import shutil
import os
import util
import modify_notebooks_file_access as mn

reference_notebook = "datascience-to-pandas"
VERBOSE = False
OTTER_VERSION = "5.5.0"
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
    util.add_sequential_ids_to_notebook(f"{notebooks_path}/{file_no_ext}.ipynb", file_no_ext)
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
        "create_pdfs": True,
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
    cr.copy_assets(assign_type, file_no_ext, True, assign_args["create_pdfs"])


def handle_non_otter_lectures(file_no_ext):
    assign_args = {
        "verbose": VERBOSE,
        "assign_type": "lec",
        "file_no_ext": file_no_ext,
        "otter_version": OTTER_VERSION,
        "data_8_repo_url": COLAB_CLONE_REPO,
        "colab_materials_repo": COLAB_REPO_MATERIALS,
        "assets_url": 'https://ds-modules.github.io/materials-sp22-assets'
    }
    assets_path = f"{os.getcwd()}/notebooks_assets/lec"
    for local_notebooks_folder in ["notebooks", "notebooks_no_footprint"]:
        raw_path = f"{os.getcwd()}/_notebooks_raw/lec/"
        notebooks_path = f"{os.getcwd()}/{local_notebooks_folder}/lec"
        binder_path = f"{os.getcwd()}/{local_notebooks_folder}_binder/lec"
        jl_path = f"{os.getcwd()}/{local_notebooks_folder}_jupyterlite/lec"
        colab_path = f"{os.getcwd()}/{local_notebooks_folder}_colab/lec"
        if not os.path.exists(notebooks_path):
            os.makedirs(notebooks_path)
        if not os.path.exists(binder_path):
            os.makedirs(binder_path)
        if not os.path.exists(jl_path):
            os.makedirs(jl_path)
        if not os.path.exists(colab_path):
            os.makedirs(colab_path)
        if not os.path.exists(assets_path):
            os.makedirs(assets_path)
        for _, _, files in os.walk(raw_path):
            for file in files:
                if "ipynb" in file and f"{file_no_ext}.ipynb" == file:
                    os.makedirs(notebooks_path, exist_ok=True)
                    os.makedirs(binder_path, exist_ok=True)
                    os.makedirs(jl_path, exist_ok=True)
                    os.makedirs(colab_path, exist_ok=True)
                    shutil.copyfile(f"{raw_path}/{file}", f"{notebooks_path}/{file}")
                    if "_no_footprint" in local_notebooks_folder:
                        mn.provide_url_in_notebook(assign_args, local_notebooks_folder)
                    shutil.copyfile(f"{notebooks_path}/{file}", f"{binder_path}/{file}")
                    shutil.copyfile(f"{notebooks_path}/{file}", f"{jl_path}/{file}")
                    shutil.copyfile(f"{notebooks_path}/{file}", f"{colab_path}/{file}")

                    util.strip_unnecessary_keys(f"{notebooks_path}/{file_no_ext}.ipynb")
                    util.add_sequential_ids_to_notebook(f"{notebooks_path}/{file_no_ext}.ipynb", file_no_ext)

                    insert_headers = [
                        "# The pip install can take a minute\n",
                        "%pip install -q datascience==0.17.5\n"
                    ]
                    util.process_ipynb(f"{binder_path}/{file_no_ext}.ipynb", insert_headers)
                    util.strip_unnecessary_keys(f"{binder_path}/{file_no_ext}.ipynb")
                    util.add_sequential_ids_to_notebook(f"{binder_path}/{file_no_ext}.ipynb", file_no_ext)

                    # insert jupyterlite
                    insert_headers = [
                        "# The pip install can take a minute\n",
                        "%pip install -q urllib3<2.0 datascience ipywidgets\n",
                        "import pyodide_http\n",
                        "pyodide_http.patch_all()\n"
                    ]
                    util.process_ipynb(f"{jl_path}/{file_no_ext}.ipynb", insert_headers)
                    util.add_sequential_ids_to_notebook(f"{jl_path}/{file_no_ext}.ipynb", file_no_ext)

                    util.colab_first_cell(assign_args, colab_path, f"{file_no_ext}.ipynb", "colab-header.txt", local_notebooks_folder)
                    util.add_sequential_ids_to_notebook(f"{colab_path}/{file_no_ext}.ipynb", file_no_ext)
                    cr.copy_assets(assign_args["assign_type"], file_no_ext, False, False)
                elif "ipynb" not in file:
                    if "_no_footprint" in local_notebooks_folder:
                        shutil.copyfile(f"{raw_path}/{file}", f"{assets_path}/{file}")
                    else:
                        shutil.copyfile(f"{raw_path}/{file}", f"{notebooks_path}/{file}")
                        shutil.copyfile(f"{notebooks_path}/{file}", f"{binder_path}/{file}")
                        shutil.copyfile(f"{notebooks_path}/{file}", f"{jl_path}/{file}")
                        shutil.copyfile(f"{notebooks_path}/{file}", f"{colab_path}/{file}")


def handle_non_otter_reference(file_no_ext):
    assign_args = {
        "verbose": VERBOSE,
        "assign_type": "reference",
        "file_no_ext": file_no_ext,
        "otter_version": OTTER_VERSION,
        "data_8_repo_url": COLAB_CLONE_REPO,
        "colab_materials_repo": COLAB_REPO_MATERIALS,
        "assets_url": 'https://ds-modules.github.io/materials-sp22-assets'
    }
    assets_path = f"{os.getcwd()}/notebooks_assets/reference/{file_no_ext}"
    for local_notebooks_folder in ["notebooks", "notebooks_no_footprint"]:
        raw_path = f"{os.getcwd()}/_notebooks_raw/reference/{file_no_ext}/"
        notebooks_path = f"{os.getcwd()}/{local_notebooks_folder}/reference/{file_no_ext}"
        binder_path = f"{os.getcwd()}/{local_notebooks_folder}_binder/reference/{file_no_ext}"
        jl_path = f"{os.getcwd()}/{local_notebooks_folder}_jupyterlite/reference/{file_no_ext}"
        colab_path = f"{os.getcwd()}/{local_notebooks_folder}_colab/reference/{file_no_ext}"

        if os.path.exists(notebooks_path):
            shutil.rmtree(notebooks_path)
        if os.path.exists(binder_path):
            shutil.rmtree(binder_path)
        if os.path.exists(jl_path):
            shutil.rmtree(jl_path)
        if os.path.exists(colab_path):
            shutil.rmtree(colab_path)

        if "_no_footprint" in local_notebooks_folder:
            for root, dir, files in os.walk(raw_path):
                for file in files:
                    if "ipynb" in file:
                        os.makedirs(notebooks_path, exist_ok=True)
                        os.makedirs(binder_path, exist_ok=True)
                        os.makedirs(jl_path, exist_ok=True)
                        os.makedirs(colab_path, exist_ok=True)
                        shutil.copyfile(f"{raw_path}/{file}", f"{notebooks_path}/{file}")
                        mn.provide_url_in_notebook(assign_args, local_notebooks_folder)
                        shutil.copyfile(f"{notebooks_path}/{file}", f"{binder_path}/{file}")
                        shutil.copyfile(f"{notebooks_path}/{file}", f"{jl_path}/{file}")
                        shutil.copyfile(f"{notebooks_path}/{file}", f"{colab_path}/{file}")
                    else:
                        if "DS_Store" not in file:
                            os.makedirs(assets_path, exist_ok=True)
                            shutil.copyfile(f"{raw_path}/{file}", f"{assets_path}/{file}")
        else:
            shutil.copytree(raw_path, notebooks_path)
            shutil.copytree(raw_path, binder_path)
            shutil.copytree(raw_path, jl_path)
            shutil.copytree(raw_path, colab_path)

        util.strip_unnecessary_keys(f"{notebooks_path}/{file_no_ext}.ipynb")
        util.add_sequential_ids_to_notebook(f"{notebooks_path}/{file_no_ext}.ipynb", file_no_ext)

        insert_headers = [
            "# The pip install can take a minute\n",
            "%pip install -q datascience==0.17.5\n"
        ]
        util.process_ipynb(f"{binder_path}/{file_no_ext}.ipynb", insert_headers)
        util.strip_unnecessary_keys(f"{binder_path}/{file_no_ext}.ipynb")
        util.add_sequential_ids_to_notebook(f"{binder_path}/{file_no_ext}.ipynb", file_no_ext)

        # insert jupyterlite
        insert_headers = [
            "# The pip install can take a minute\n",
            "%pip install -q urllib3<2.0 datascience ipywidgets\n",
            "import pyodide_http\n",
            "pyodide_http.patch_all()\n"
        ]
        util.process_ipynb(f"{jl_path}/{file_no_ext}.ipynb", insert_headers)
        util.add_sequential_ids_to_notebook(f"{jl_path}/{file_no_ext}.ipynb", file_no_ext)

        util.colab_first_cell(assign_args, colab_path, f"{file_no_ext}.ipynb", "colab-header.txt", local_notebooks_folder)
        util.add_sequential_ids_to_notebook(f"{colab_path}/{file_no_ext}.ipynb", file_no_ext)
        cr.copy_assets("reference", file_no_ext, False, False)


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
            if assign_type == "reference":
                file_no_ext = f
            name = f"{file_no_ext}.ipynb"
            if not file or (file == name):
                if assign_type == "reference":
                    handle_non_otter_reference(file_no_ext)
                elif assign_type == "lec":
                    handle_non_otter_lectures(file_no_ext)
                    handle_non_otter_lectures(f"{file_no_ext}_0")
                else:
                    setup(assign_type, file_no_ext)
                    run_assign(assign_type, file_no_ext)
    print("The notebooks are created!")


assignments = {
    "hw": range(1, 13),
    "lab": range(1, 11),
    "project": range(1, 4),
    "lec": [1] + list(range(3, 22)) + list(range(23, 34)) + list(range(35, 40)),
    "reference": ["datascience-to-pandas"]
}

# full file name: hw02.ipynb or leave "" and it will everything in assignments dict above
run("hw03.ipynb")
