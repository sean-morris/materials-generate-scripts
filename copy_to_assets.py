import shutil
import os
import argparse

OUTPUT_FOLDER = "notebooks_assets"


# This will walk the notebooks path removing all files that are not
# ipynb files. It will also delete the d8error.py and errorConfig.json files
# All files are moved to ./assets -- they should then be copied to whatever
# location will become the publicly available spot for these files
def copy_files_assests_repo(parent_path, is_test):
    assets_path = f"{os.getcwd()}/{OUTPUT_FOLDER}"
    for folder in ["hw", "lab", "lectures", "project", "reference"]:
        for root, dirs, files in os.walk(f"{os.getcwd()}/{parent_path}/{folder}"):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = "/".join(file_path.split("/")[7:-1])
                if not is_test or (is_test and "hw01" in file_path):
                    if not file.endswith(".ipynb") and file != ".DS_Store":
                        rel_path = "/".join(file_path.split("/")[7:-1])
                        assets_rel_path = f"{assets_path}/{rel_path}"
                        os.makedirs(assets_rel_path, exist_ok=True)
                        try:
                            shutil.copy(file_path, assets_rel_path)
                        except Exception:
                            print("here")
                            pass  # already exists
                    elif file.endswith(".ipynb"):
                        raw_path = f"{os.getcwd()}/{parent_path}_no_footprint/{rel_path}"
                        os.makedirs(raw_path, exist_ok=True)
                        shutil.copy(file_path, raw_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Copy all non-notebook files out of path perserving relative paths')
    parser.add_argument('local_notebooks_folder', metavar='p', type=str, help='notebooks')
    parser.add_argument('--is_test', metavar='it', type=bool, help='if testing do one notebook', default=False, action=argparse.BooleanOptionalAction)
    args, unknown = parser.parse_known_args()
    end_path = f"{os.getcwd()}/{OUTPUT_FOLDER}/"
    if os.path.exists(end_path):
        shutil.rmtree(end_path)
    raw_path = f"{os.getcwd()}/{args.local_notebooks_folder}_no_footprint/"
    if os.path.exists(raw_path):
        shutil.rmtree(raw_path)
    copy_files_assests_repo(args.local_notebooks_folder, args.is_test)
    print(f"Assets Copied: {end_path}")
