# materials-generate-scripts
These scripts generate materials for various platforms: JupyterHub, Colab, JupyterLite
Their will be notebooks with the footprint and without for all the environments
A notebook with no footprint means that we are loading all external files(csv, png, etc) from a URL.

**convert.py: Any otter-grader v3 notebooks are converted to otter-grader v4**

# Executing all notebooks at once or one at a time
`python3 main.py` runs all the steps necessary to create the various types of notebooks

**Notice in main.py that you can run one notebook or all the notebooks in the folder _notebooks_raw**

You need to study main.py to see the configuration options. There are series of pieces to consider:
- assignments dictionary: The script runs through this structure when you do not pass in a single
notebook to be run. Notice that the keys correspond to the top-level directories in the _notebooks_raw folder. The list of numbers corresponds the assignment number for each assignment type.
- reference_notebook: the one assignment in data 8 that does not have a number on it.
- VERBOSE: If set to True you see the output from otter assign as well as some other pieces
- OTTER_VERSION: Set to 4.4.1 this is used in colab notebooks
- COLAB_*: The colab notebooks need special configuration

The `run("")` at the bottom of main.py runs the script. If you pass in a notebook name it will only
run that notebooks(e.g. `run("hw02.ipynb")`)

The `run` function either iterates over all the assignments dict or runs the process for one file. In either case, the process starts by copying the notebook from the folder, _notebooks_raw into the folder, notebooks. 

You original notebooks should be put into _notebooks_raw

# Steps
The remaining steps are detailed here but implemented in `main.py/run_assign(assign_type, file_no_ext)`

## Handle Colab with Footprint
1) **Line:** `cn.colab_assign_for_file(assign_args, "notebooks")`
2) This does the following:
  * created folders notebooks_colab
  * modifies the assignment config so the notebooks know they are colab notebooks - AssignmentConfig
  * runs otter assign to create the student and instructor notebooks needed for colab -- with footprint!
  * modifies the first cell for student and instructor notebook so that colab can connect appropriately to notebooks 
  * creates and populates the appropriate folders: e.g. notebooks_colab/hw/hw01/{student/autograder} 

## Instructions for removing FootPrint for normal and colab notebooks
3) Copy Assets
- **Line:** `ca.copy_files_assets_repo(assign_args)`

It will automatically handle the copying for the folders: notebooks and notebooks_colab
This copies all the assets from the raw folder to the notebooks_assets folder -- the assets should be exactly the same between notebooks and notebooks_colab. 


4) Copy the ./notebooks_assets folder to the publicly available web location: e.g.
materials-sp22-assets in which I allow live access via GH Pages to the main branch. This must be copied and committed before the next step

## Run colab_notebooks again for no footprint
5) **Line:** `cn.colab_assign_for_file(assign_args, "notebooks_no_footprint")`
   if and when you are running otter assign for no_footprint this happens:
       * Removes the files attribute from the Assignment Config
       * Replaces each file reference in the notebook with public_url path to the file

## Run otter assign to create notebooks for no footprint and then with footprint
6) Run otter assign
   * **Line:**  `oa.assign(assign_args, "notebooks_no_footprint", create_pdfs=False)`
   * **Line:**  `oa.assign(assign_args, "notebooks", create_pdfs=assign_args["create_pdfs"])`

## Run jupyterlite_create
7) Create JL notebooks
   * **Line:**  `jc.jupyterlite(assign_args, "notebooks")`
   * **Line:**  `jc.jupyterlite(assign_args, "notebooks_no_footprint")`

## Run binder_create for no footprint and then with footprint
8) Create binder notebooks
   * **Line:**  `bc.binderize(assign_args, "notebooks")`
   * **Line:**  `bc.binderize(assign_args, "notebooks_no_footprint")`

# Resulting folders
This section describes what is in each folder after all the commands in main.py are executed. From here, you copy the files to appropriate repositories to distribute

* notebooks: Your original set of raw unprocessed notebooks and any external files needed(csv, png, etc) as well as the results of otter assign being run on your notebooks -- each folder has a student and autograder subfolder -- this includes **footprint**
* notebooks_assets: these should be copied to a space that renders them in a publicly-viewable url; it is what will be used to load external files and images; for example we have materials-sp22-assets in the ds-modules github org
* notebook_binder: binderized student and instructor(autograder folder) notebooks for each assignment **with** footprint
* notebook_colab: colab-enabled student and instructor(autograder folder) notebooks for each assignment **with** footprint
* notebook_jupyterlite: jupyterlite-enabled student and instructor(autograder folder) notebooks for each assignment **with** footprint
* notebook_jupyterlite: jupyterlite-enabled student and instructor(autograder folder) notebooks for each assignment **with** footprint

* notebooks_no_footprint: the results of otter assign being run on your notebooks -- each folder has a student and autograder subfolder -- there is **no footprint**
* notebook_no_footprint_binder: binderized student and instructor(autograder folder) notebooks for each assignment **without** footprint
* notebook_no_footprint_colab: colab-enabled student and instructor(autograder folder) notebooks for each assignment **without** footprint
* notebook_no_footprint_jupyterlite: jupyterlite-enabled student and instructor(autograder folder) notebooks for each assignment **without** footprint