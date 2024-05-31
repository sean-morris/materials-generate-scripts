import shutil
import os

OUTPUT_FOLDER = "notebooks_assets"


# This will walk the notebooks path removing all files that are not
# ipynb files. It will also delete the d8error.py and errorConfig.json files
# All files are moved to ./assets -- they should then be copied to whatever
# location will become the publicly available spot for these files
def copy_files_assests_repo(a_args):
    assets_path = f"{os.getcwd()}/{OUTPUT_FOLDER}/{a_args['assign_type']}/{a_args['file_no_ext']}"
    assignment_source_path = f"{os.getcwd()}/notebooks/{a_args['assign_type']}/{a_args['file_no_ext']}"
    if not os.path.exists(assets_path):
        os.makedirs(assets_path)
    else:
        shutil.rmtree(assets_path)

    for _, _, files in os.walk(assignment_source_path):
        for file in files:
            file_extension = os.path.splitext(file)[1]
            if file_extension not in [".ipynb", ""]:
                src_file = os.path.join(assignment_source_path, file)
                dest_file = os.path.join(assets_path, file)

                dest_file_dir = os.path.dirname(dest_file)
                if not os.path.exists(dest_file_dir):
                    os.makedirs(dest_file_dir)

                shutil.copy2(src_file, dest_file)
    print(f"Copied Assets: {a_args['assign_type']}/{a_args['file_no_ext']}")
