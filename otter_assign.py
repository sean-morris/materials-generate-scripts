from subprocess import run
import argparse
import os
import shutil
from util import remove_otter_assign_output, strip_unnecessary_keys


def assign(local_notebooks_folder, create_pdfs, is_test, run_otter_tests, test_notebook):
    for folder in ["hw", "lab", "project", "reference"]:
        for root, dirs, files in os.walk(f"{os.getcwd()}/{local_notebooks_folder}/{folder}"):
            for file in files:
                if (not is_test and file.endswith(".ipynb")) or (is_test and file == test_notebook):
                    file_path = os.path.join(root, file)
                    dir_path = "/".join(file_path.split("/")[:-1])
                    assign_args = ["otter", "assign", "-v"]
                    if not create_pdfs:
                        assign_args.append("--no-pdfs")
                    if not run_otter_tests:
                        assign_args.append("--no-run-tests")
                    assign_args.append(file_path)
                    assign_args.append(dir_path)
                    otter_assign_out = run(assign_args, capture_output=True)
                    out = (otter_assign_out.stdout).decode("utf-8")
                    err = (otter_assign_out.stderr).decode("utf-8")
                    msg = "All autograder tests passed"
                    if msg in out or msg in err:
                        print(f"Hub: {local_notebooks_folder}: Tests Passed: {file}")
                    else:
                        print(f"Hub: {local_notebooks_folder}: Tests NOT Passed: {file}")
                        with open(f"{os.getcwd()}/otter_assign_log_{local_notebooks_folder}.txt", "a") as f:
                            f.write(err)
                    remove_otter_assign_output(dir_path)
                    strip_unnecessary_keys(f"{dir_path}/student/{file}")
                    strip_unnecessary_keys(f"{dir_path}/autograder/{file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run otter assign on folder of notebooks')
    parser.add_argument('local_notebooks_folder', metavar='p', type=str, help='notebooks_no_footprint')
    parser.add_argument('--create_pdfs', metavar='cp', type=bool, help='are we creating PDFS', default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument('--is_test', metavar='it', type=bool, help='if testing do one notebook', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--run_otter_tests', metavar='ot', type=bool, help='This means when otter assign is executed we double check the tests pass', default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument('test_notebook', metavar='p', type=str, help='hw03.ipynb')
    args, unknown = parser.parse_known_args()
    log_path = f"{os.getcwd()}/otter_assign_log_{args.local_notebooks_folder}.txt"
    if os.path.exists(log_path):
        os.remove(log_path)

    assign(args.local_notebooks_folder, args.create_pdfs, args.is_test, args.run_otter_tests, args.test_notebook)
