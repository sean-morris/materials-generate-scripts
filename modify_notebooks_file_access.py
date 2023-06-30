import os
import json
import argparse


def remove_files_config(nb_json):
    config_cell = nb_json["cells"][0]
    src = config_cell["source"]
    new_src = []
    files = False
    for e in src:
        if files:
            if "-" in e:
                continue
            else:
                files = False
        if "files:\n" in e:
            files = True
        else:
            new_src.append(e)
    nb_json["cells"][0]["source"] = new_src


def remove_d8error_import(nb_json):
    recursive_search_and_replace(nb_json, "import d8error", "")


# the handling of local files uses the open() as opposed to need to urlopen
# lab05 of data 8 is one example where this is a problem. A bit fragile here.
def handle_text_file_open(elem):
    elem = elem.replace("open", "urlopen")
    elem = elem.replace(", encoding='utf-8'", "")
    elem = elem.replace(".read()", ".read().decode('utf-8')")
    elem = "from urllib.request import urlopen\n" + elem
    return elem


def recursive_search_and_replace(dictionary, search_value, replace_value):
    for cell in dictionary["cells"]:
        for index, elem in enumerate(cell["source"]):
            if search_value in elem:
                x = elem.index(search_value)
                is_full_word = elem[x-1:x] != "_"  # this handle file names like good_movies.csv and movies.csv
                if is_full_word:
                    elem = elem.replace(search_value, replace_value)
                    if ".txt" in search_value:
                        elem = handle_text_file_open(elem)
                    cell["source"][index] = elem


def provide_url_in_notebook(parent_path, public_url):
    for folder in ["hw", "lab", "lectures", "project", "reference"]:
        for root, dirs, files in os.walk(f"{os.getcwd()}/{parent_path}/{folder}"):
            for file in files:
                if file.endswith(".ipynb"):
                    file_path = os.path.join(root, file)
                    rel_path = "/".join(file_path.split("/")[7:-1])
                    assets_path = f"{os.getcwd()}/notebooks_assets/{rel_path}"
                    with open(file_path, 'r') as nb:
                        nb_json = json.load(nb)
                    remove_files_config(nb_json)
                    for r, d, fs in os.walk(assets_path):
                        for a in fs:
                            url_rel_path = "/".join(r.split("/")[7:])
                            url_path = f"{public_url}/{url_rel_path}/{a}"
                            remove_d8error_import(nb_json)
                            recursive_search_and_replace(nb_json, a, url_path)

                    with open(file_path, 'w+') as target:
                        json.dump(nb_json, target, indent=3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Modify raw notebooks -- removing files from Assignment Config and changing paths to file')
    parser.add_argument('local_notebooks_folder', metavar='p', type=str, help='notebooks_no_footprint')
    parser.add_argument('public_url', metavar='p', type=str, help='https://ds-modules.github.io/materials-sp22-assets')
    args, unknown = parser.parse_known_args()
    provide_url_in_notebook(args.local_notebooks_folder, args.public_url)
