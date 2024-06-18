import shutil
import glob
import os
import fnmatch

PARENT_PARTIAL = "materials-sp22"
ROOT_PATH = "/Users/sean/Documents/cb"


def delete_and_copy(src, dest, delete_first):
    if delete_first:
        shutil.rmtree(dest, ignore_errors=True)
    if os.path.exists(src):
        shutil.copytree(src, dest, dirs_exist_ok=True)


def copy_assets(assign_type, file_no_ext, copy_autograder, copy_pdfs):
    rel_path = f"{assign_type}/{file_no_ext}"
    student_path = "student"
    delete_first = True
    if assign_type == "lec":
        rel_path = f"{assign_type}"
        student_path = ""
        delete_first = False
    if assign_type == "reference":
        rel_path = f"{assign_type}"
        student_path = ""

    # copy notebooks_assets to materials-sp22-assets
    src = f"notebooks_assets/{rel_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-assets/{rel_path}"
    if os.path.exists(src):
        delete_and_copy(src, dest, delete_first)

    # copy notebooks/assign/student to materials-sp22
    src = f"notebooks/{rel_path}/{student_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_no_footprint to materials-sp22-no-footprint
    src = f"notebooks_no_footprint/{rel_path}/{student_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-no-footprint/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_colab to materials-sp22-colab
    src = f"notebooks_colab/{rel_path}/{student_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-colab/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_no_footprint_colab to materials-sp22-colab-no-footprint
    src = f"notebooks_no_footprint_colab/{rel_path}/{student_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-colab-no-footprint/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_binder to materials-sp22-binder
    src = f"notebooks_binder/{rel_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-binder/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_no_footprint_binder to materials-sp22-binder-no-footprint
    src = f"notebooks_no_footprint_binder/{rel_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-binder-no-footprint/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_jupyterlite to materials-sp22-jupyterlite
    src = f"notebooks_jupyterlite/{rel_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-jupyterlite/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks_no_footprint_jupyterlite to materials-sp22-jupyterlite-no-footprint
    src = f"notebooks_no_footprint_jupyterlite/{rel_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-jupyterlite-no-footprint/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy notebooks/assign/autograder to materials-sp22-private
    # copy autograder.zip
    if copy_autograder:
        src_pattern = f"notebooks/{rel_path}/autograder/*.zip"
        dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-private/autograder_zips/{rel_path}/autograder.zip"
        file_to_copy = glob.glob(src_pattern)
        if os.path.exists(dest):
            os.remove(dest)
        for file_path in file_to_copy:
            shutil.copy(file_path, dest)

    # copy solutions
    if copy_pdfs:
        src = f"notebooks/{rel_path}/autograder/{file_no_ext}-sol.pdf"
        dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-private/solutions_pdfs/{rel_path}/{file_no_ext}.pdf"
        if os.path.exists(dest):
            os.remove(dest)
        if os.path.exists(src):
            shutil.copy(src, dest)

    # copy raw_notebook back -- in case changes made
    src = f"_notebooks_raw/{rel_path}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-private/raw_notebooks/{rel_path}"
    delete_and_copy(src, dest, delete_first)

    # copy instructor_notebooks
    src = f"notebooks/{rel_path}/autograder"
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
