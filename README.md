# materials-generate-scripts
These scripts generate materials for various platforms: JupyterHub, Colab, JupyterLite
Their will be notebooks with the footprint and without for all the environments
A notebook with no footprint means that we are loading all external files(csv, png, etc) from a URL.

**Conversion of otterized notebooks from (otter-3)v0 to (otter-4)v1: convert.py**

# Executing at once
`sh ./main.sh` runs all the steps necessary to create the various types of notebooks

**Notice in ./main.sh that if you include --is_test it will only run for hw01; --no-is_test will run all**

# Steps
## First Steps
1) Copy raw/original notebooks from materials-xxx-private to this repo into the folder notebooks

## Handle Colab with Footprint
2) **Execute:** `python3 colab_notebooks.py notebooks 4.3.4 https://github.com/data-8 materials-sp22`
3) This does the following:
  * created folders notebooks_colab
  * modifies the assignment config so the notebooks know they are colab notebooks - AssignmentConfig
  * runs otter assign to create the student and instructor notebooks needed for colab -- with footprint!
  * modifies the first cell for student and instructor notebook so that colab can connect appropriately to notebooks * creates these folders: notebooks_colab_footprint{_student/_instructor} -- these are colab notebooks that carry the footprint

## Instructions for removing FootPrint for normal and colab notebooks
4) Run copy_to_assets.py [name_of_folder_of_notebooks]: 
- **Execute:** `python3 copy_to_assets.py notebooks`

It will automatically handle the copying for the folders: notebooks and notebooks_colab
This copies all the assets from the raw folder to the notebooks_assets folder -- the assets should be exactly the same between notebooks and notebooks_colab. It will also copy the raw notebooks by themselves to notebooks_no_footprint and notebooks_colab_no_footprint


5) Copy the ./notebooks_assets folder to the publicly available web location: e.g.
materials-sp22-assets in which I allow live access via GH Pages to the main branch. This must be copied and committed before the next step

## Modifying Notebooks to use remote external files and removing "import d8error" from notebook
6) Run modify_notebooks_file_access.py [name_of_folder_of_notebooks] [public_url]: 
    * **Execute:** `python3 modify_notebooks_file_access.py notebooks_no_footprint https://ds-modules.github.io/materials-sp22-assets`
    * **Execute:** `python3 modify_notebooks_file_access.py notebooks_colab_no_footprint https://ds-modules.github.io/materials-sp22-assets`
        
   * This does the following:
       * This removes the files attribute from the Assignment Config
       * Replaces each file reference in the notebook with public_url path to the file
       * Removes the "import d8error" line from the notebook

## Run colab_notebooks again for no footprint
8) **Execute:** `python3 colab_notebooks.py notebooks_no_footprint 4.3.4 https://github.com/data-8 materials-sp22`

## Run otter assign to create notebooks for no footprint and then with footprint
9) Run python3 otter_assign.py [name_of_folder_of_notebooks_no_footprint]
   * **Execute:**  `python3 otter_assign.py notebooks_no_footprint`
   * **Execute:**  `python3 otter_assign.py notebooks`

## Run jupyterlite_create for no footprint and then with footprint
10) Run python3 jupyterlite_create.py [name_of_folder_of_notebooks_no_footprint] [otter_version]
   * **Execute:**  `python3 jupyterlite_create.py notebooks 4.3.4`
   * **Execute:**  `python3 jupyterlite_create.py notebooks_no_footprint 4.3.4`

## Run binder_create for no footprint and then with footprint
11) Run python3 binder_create.py [name_of_folder_of_notebooks_no_footprint] [otter_version]
   * **Execute:**  `python3 binder_create.py notebooks 4.3.4`
   * **Execute:**  `python3 binder_create.py notebooks_no_footprint 4.3.4`

# Resulting folders
This section describes what is in each folder after all the commands in ./main.sh are executed. From here, you copy the files to appropriate repositories to distribute

* notebooks: Your original set of raw unprocessed notebooks and any external files needed(csv, png, etc)
* notebooks_assets: these should be copied to a space that renders them in a publicly-viewable url; it is what will be used to load external files and images; for example we have materials-sp22-assets in the ds-modules github
* notebooks_normal: the results of otter assign being run on your notebooks -- each folder has a student and autograder subfolder -- this includes **footprint**
* notebook_binder: binderized student and instructor(autograder folder) notebooks for each assignment **with** footprint
* notebook_colab: colab-enabled student and instructor(autograder folder) notebooks for each assignment **with** footprint
* notebook_jupyterlite: jupyterlite-enabled student and instructor(autograder folder) notebooks for each assignment **with** footprint
* notebook_jupyterlite: jupyterlite-enabled student and instructor(autograder folder) notebooks for each assignment **with** footprint

* notebooks_no_footprint: the results of otter assign being run on your notebooks -- each folder has a student and autograder subfolder -- there is **no footprint**
* notebook_no_footprint_binder: binderized student and instructor(autograder folder) notebooks for each assignment **without** footprint
* notebook_no_footprint_colab: colab-enabled student and instructor(autograder folder) notebooks for each assignment **without** footprint
* notebook_no_footprint_jupyterlite: jupyterlite-enabled student and instructor(autograder folder) notebooks for each assignment **without** footprint