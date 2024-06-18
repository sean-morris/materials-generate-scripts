from subprocess import run
import os
import modify_notebooks_file_access as mn
from util import remove_otter_assign_output, strip_unnecessary_keys, setup_assign_dir, add_sequential_ids_to_notebook


def assign(a_args, local_notebooks_folder, create_pdfs=False):
    assign_path = f"{os.getcwd()}/{local_notebooks_folder}/{a_args['assign_type']}/{a_args['file_no_ext']}"
    file_name = f"{a_args['file_no_ext']}.ipynb"
    file_path = os.path.join(assign_path, file_name)
    setup_assign_dir(a_args, assign_path)
    if "no_footprint" in local_notebooks_folder:
        mn.provide_url_in_notebook(a_args, local_notebooks_folder)
    assign_args = ["otter", "assign", "-v"]
    if not create_pdfs:
        assign_args.append("--no-pdfs")
    if not a_args["run_otter_tests"]:
        assign_args.append("--no-run-tests")
    assign_args.append(file_path)
    assign_args.append(assign_path)
    add_sequential_ids_to_notebook(file_path, a_args['file_no_ext'])
    otter_assign_out = run(assign_args, capture_output=True)
    out = (otter_assign_out.stdout).decode("utf-8")
    err = (otter_assign_out.stderr).decode("utf-8")
    if a_args["verbose"]:
        print(out)
        print(err)

    msg = "All autograder tests passed"
    if msg in out or msg in err:
        print(f"Hub: {local_notebooks_folder}: Tests Passed: {file_name}")
    else:
        print(f"Hub: {local_notebooks_folder}: Tests NOT Passed: {file_name}")
        with open(f"{os.getcwd()}/otter_assign_log_{local_notebooks_folder}.txt", "a") as f:
            f.write(err)
    remove_otter_assign_output(assign_path)
    strip_unnecessary_keys(f"{assign_path}/student/{file_name}")
    strip_unnecessary_keys(f"{assign_path}/autograder/{file_name}")
    add_sequential_ids_to_notebook(f"{assign_path}/student/{file_name}", a_args['file_no_ext'])
    add_sequential_ids_to_notebook(f"{assign_path}/autograder/{file_name}", a_args['file_no_ext'])
