import os
import json


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


def provide_url_in_notebook(a_args):
    file_path = f"{os.getcwd()}/notebooks_no_footprint_colab/{a_args['assign_type']}/{a_args['file_no_ext']}/{a_args['file_no_ext']}.ipynb"
    assets_path = f"{os.getcwd()}/notebooks_assets/{a_args['assign_type']}/{a_args['file_no_ext']}"
    with open(file_path, 'r') as nb:
        nb_json = json.load(nb)
    remove_files_config(nb_json)
    for r, _, fs in os.walk(assets_path):
        for a in fs:
            url_path = f"{a_args['assets_url']}/{a_args['assign_type']}/{a_args['file_no_ext']}/{a}"
            remove_d8error_import(nb_json)
            recursive_search_and_replace(nb_json, a, url_path)

    with open(file_path, 'w+') as target:
        json.dump(nb_json, target, indent=3)
    print(f"Added Public URL - no_footprint_colab: {a_args['assign_type']}/{a_args['file_no_ext']}")
