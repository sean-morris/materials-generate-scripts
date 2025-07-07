import shutil
import glob
import os
import fnmatch

PARENT_PARTIAL = "materials-fds"
ROOT_PATH = "/Users/sean/Documents/data-8"


def delete_and_copy(src, dest, delete_first):
    if delete_first:
        shutil.rmtree(dest, ignore_errors=True)
    if os.path.exists(src):
        shutil.copytree(src, dest, dirs_exist_ok=True)


def copy_assets(assign_type, file_no_ext, copy_autograder, copy_pdfs):
    rel_path = f"{assign_type}/{file_no_ext}"
    src_rel_path = rel_path
    student_path = "student"
    delete_first = True
    if assign_type == "lec":
        src_rel_path = "lec"
        rel_path = "lectures"
        student_path = ""
        delete_first = False
    if assign_type == "reference":
        src_rel_path = "reference"
        rel_path = f"{assign_type}"
        student_path = ""

    # copy notebooks_assets to materials-fds-assets
    src = f"notebooks_assets/{src_rel_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-assets/{src_rel_path}"
    if os.path.exists(src):
        delete_and_copy(src, dest, delete_first)

    # copy notebooks/assign/student to materials-fds
    src = f"notebooks/{src_rel_path}/{student_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_no_footprint to materials-fds-no-footprint
    src = f"notebooks_no_footprint/{src_rel_path}/{student_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-no-footprint/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_colab to materials-fds-colab
    src = f"notebooks_colab/{src_rel_path}/{student_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-colab/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_no_footprint_colab to materials-fds-colab-no-footprint
    src = f"notebooks_no_footprint_colab/{src_rel_path}/{student_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-colab-no-footprint/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_binder to materials-fds-binder
    src = f"notebooks_binder/{src_rel_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-binder/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_no_footprint_binder to materials-fds-binder-no-footprint
    src = f"notebooks_no_footprint_binder/{src_rel_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-binder-no-footprint/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_jupyterlite to materials-fds-jupyterlite
    src = f"notebooks_jupyterlite/{src_rel_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-jupyterlite/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_no_footprint_jupyterlite to materials-fds-jupyterlite-no-footprint
    src = f"notebooks_no_footprint_jupyterlite/{src_rel_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-jupyterlite-no-footprint/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks/assign/autograder to materials-fds-private
    # copy autograder.zip
    if copy_autograder:
        src_pattern = f"notebooks/{src_rel_path}/autograder/*.zip"
        dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-private/autograder_zips/{rel_path}"
        file_to_copy = glob.glob(src_pattern)
        if os.path.exists(dest):
            zip_files = glob.glob(os.path.join(dest, "*.zip"))
            if not zip_files:
                print(f"No .zip files found in {dest}")
            else:
                print(f"Found .zip files to delete in {dest}:")
                for file_path in zip_files:
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        print(f"  Error deleting {file_path}: {e}")

        for file_path in file_to_copy:
            shutil.copy(file_path, dest)

    # copy solutions
    if copy_pdfs:
        src = f"notebooks/{src_rel_path}/autograder/{file_no_ext}-sol.pdf"
        dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-private/solutions_pdfs/{rel_path}/{file_no_ext}.pdf"
        if os.path.exists(dest):
            os.remove(dest)
        if os.path.exists(src):
            shutil.copy(src, dest)

    # copy raw_notebook back -- in case changes made
    src = f"_notebooks_raw/{src_rel_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-private/raw_notebooks/{src_rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy instructor_notebooks
    src = f"notebooks/{src_rel_path}/autograder"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-private/instructor_notebooks/{rel_path}"
    shutil.rmtree(dest, ignore_errors=True)
    os.makedirs(dest, exist_ok=True)
    for root, _, files in os.walk(src):
        # Copy files, excluding those that match the exclude patterns
        for file in files:
            if not any(fnmatch.fnmatch(file, pattern) for pattern in ['*.zip', '*-sol.pdf', '*.pyc']):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dest, file)
                shutil.copy2(src_file, dst_file)

    print(f"Files Copied for: {file_no_ext}")
