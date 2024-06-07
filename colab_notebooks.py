import os
import json
from subprocess import run
from util import process_ipynb, remove_otter_assign_output, strip_unnecessary_keys, setup_assign_dir
import modify_notebooks_file_access as mn


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


def assign(a_args, root_path, file, pdfs, footprint, run_otter_tests):
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
    if a_args["verbose"]:
        print(out)
        print(err)
    msg = "All autograder tests passed"
    if not run_otter_tests:
        print(f"Colab {footprint}: Complete: Tests NOT Run: {file}")
    elif msg in out or msg in err:
        print(f"Colab {footprint}: Tests Passed: {file}")
    else:
        print(f"Colab {footprint}: Tests NOT Passed: {file}")
        with open(f"{os.getcwd()}/colab_assign_log_{file}.txt", "a") as f:
            f.write(err)


def colab_first_cell(args, root_path, file, header_file, local_notebooks_folder):
    otter_version = args["otter_version"]
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
            line = line.replace("||OTTER_GRADER_VERSION||", otter_version)
            line = line.replace("||CLONE_REPO_PATH||", clone_repo_path)
            line = line.replace("||ORIGINAL_MATERIALS_REPO||", f"{materials_repo}")
            line = line.replace("||NOTEBOOK_DIR||", notebook_path)
            insert_headers.append(line)
    process_ipynb(file_path, insert_headers)


def colab_assign_for_file(a_args, local_notebooks_folder):
    assign_path = f"{os.getcwd()}/{local_notebooks_folder}_colab/{a_args['assign_type']}/{a_args['file_no_ext']}"
    file_name = f"{a_args['file_no_ext']}.ipynb"
    setup_assign_dir(a_args, assign_path)
    if "no_footprint" in local_notebooks_folder:
        mn.provide_url_in_notebook(a_args, f"{local_notebooks_folder}_colab")
    change_colab_assignment_config(assign_path, file_name)  # adds runs_on
    assign(a_args, assign_path, file_name, a_args["create_pdfs"], local_notebooks_folder, a_args["run_otter_tests"])
    colab_first_cell(a_args, f"{assign_path}/student", file_name, "colab-header.txt", local_notebooks_folder)
    colab_first_cell(a_args, f"{assign_path}/autograder", file_name, "colab-header.txt", local_notebooks_folder)
    remove_otter_assign_output(assign_path)
    strip_unnecessary_keys(f"{assign_path}/student/{file_name}")


def colab_handle_lectures(a_args, local_nb_folder):
    new_path = f"{os.getcwd()}/{local_nb_folder}_lectures_colab"
    colab_first_cell(a_args, new_path, f"{a_args['file_no_ext']}.ipynb", "colab-header-lectures.txt", local_nb_folder)
    print(f"Colab Lectures: {a_args['file_no_ext']} completed")
