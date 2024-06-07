import shutil
import glob
import os
import fnmatch

PARENT_PARTIAL = "materials-sp22"
ROOT_PATH = "/Users/sean/Documents/cb"


def delete_and_copy(src, dest):
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(src, dest)


def copy_assets(assign_type, file_no_ext):
    # copy notebooks_assets to materials-sp22-assets
    src = f"notebooks_assets/{assign_type}/{file_no_ext}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-assets/{assign_type}/{file_no_ext}"
    delete_and_copy(src, dest)

    # copy notebooks/assign/student to materials-sp22
    src = f"notebooks/{assign_type}/{file_no_ext}/student"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}/{assign_type}/{file_no_ext}"
    delete_and_copy(src, dest)

    # copy notebooks_no_footprint to materials-sp22-no-footprint
    src = f"notebooks_no_footprint/{assign_type}/{file_no_ext}/student"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-no-footprint/{assign_type}/{file_no_ext}"
    delete_and_copy(src, dest)

    # copy notebooks_colab to materials-sp22-colab
    src = f"notebooks_colab/{assign_type}/{file_no_ext}/student"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-colab/{assign_type}/{file_no_ext}"
    delete_and_copy(src, dest)

    # copy notebooks_no_footprint_colab to materials-sp22-colab-no-footprint
    src = f"notebooks_no_footprint_colab/{assign_type}/{file_no_ext}/student"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-colab-no-footprint/{assign_type}/{file_no_ext}"
    delete_and_copy(src, dest)

    # copy notebooks_binder to materials-sp22-binder
    src = f"notebooks_binder/{assign_type}/{file_no_ext}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-binder/{assign_type}/{file_no_ext}"
    delete_and_copy(src, dest)

    # copy notebooks_no_footprint_binder to materials-sp22-binder-no-footprint
    src = f"notebooks_no_footprint_binder/{assign_type}/{file_no_ext}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-binder-no-footprint/{assign_type}/{file_no_ext}"
    delete_and_copy(src, dest)

    # copy notebooks_jupyterlite to materials-sp22-jupyterlite
    src = f"notebooks_jupyterlite/{assign_type}/{file_no_ext}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-jupyterlite/{assign_type}/{file_no_ext}"
    delete_and_copy(src, dest)

    # copy notebooks_no_footprint_jupyterlite to materials-sp22-jupyterlite-no-footprint
    src = f"notebooks_no_footprint_jupyterlite/{assign_type}/{file_no_ext}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-jupyterlite-no-footprint/{assign_type}/{file_no_ext}"
    delete_and_copy(src, dest)

    # copy notebooks/assign/autograder to materials-sp22-private
    # copy autograder.zip
    src_pattern = f"notebooks/{assign_type}/{file_no_ext}/autograder/*.zip"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-private/autograder_zips/{assign_type}/{file_no_ext}/autograder.zip"
    file_to_copy = glob.glob(src_pattern)
    if os.path.exists(dest):
        os.remove(dest)
    for file_path in file_to_copy:
        shutil.copy(file_path, dest)

    # copy solutions
    src = f"notebooks/{assign_type}/{file_no_ext}/autograder/{file_no_ext}-sol.pdf"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-private/solutions_pdfs/{assign_type}/{file_no_ext}/{file_no_ext}.pdf"
    if os.path.exists(dest):
        os.remove(dest)
    if os.path.exists(src):
        shutil.copy(src, dest)

    # copy raw_notebook back -- in case changes made
    src = f"_notebooks_raw/{assign_type}/{file_no_ext}"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-private/raw_notebooks/{assign_type}/{file_no_ext}"
    delete_and_copy(src, dest)

    # copy instructor_notebooks
    src = f"notebooks/{assign_type}/{file_no_ext}/autograder"
    dest = f"{ROOT_PATH}/{PARENT_PARTIAL}-private/instructor_notebooks/{assign_type}/{file_no_ext}"
    shutil.rmtree(dest, ignore_errors=True)
    os.makedirs(dest, exist_ok=True)
    for root, _, files in os.walk(src):
        # Copy files, excluding those that match the exclude patterns
        for file in files:
            if not any(fnmatch.fnmatch(file, pattern) for pattern in ['*.zip', '*-sol.pdf']):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dest, file)
                shutil.copy2(src_file, dst_file)

    print(f"Files Copied for: {file_no_ext}")
