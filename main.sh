OTTER_VERSION=4.3.4
COLAB_CLONE_REPO=https://github.com/data-8
COLAB_REPO_MATERIALS=materials-sp22-colab
NOTEBOOKS=notebooks
NOTEBOOKS_NO_FOOTPRINT=notebooks_no_footprint
ASSETS_URL=https://ds-modules.github.io/materials-sp22-assets
TEST=--is_test  # --is_test or --no-is_test

cp -r notebooks notebooks_clean
python3 colab_notebooks.py $NOTEBOOKS $OTTER_VERSION $COLAB_CLONE_REPO $COLAB_REPO_MATERIALS $TEST
python3 copy_to_assets.py $NOTEBOOKS
python3 modify_notebooks_file_access.py $NOTEBOOKS_NO_FOOTPRINT $ASSETS_URL
python3 colab_notebooks.py $NOTEBOOKS_NO_FOOTPRINT $OTTER_VERSION $COLAB_CLONE_REPO $COLAB_REPO_MATERIALS $TEST
python3 otter_assign.py $NOTEBOOKS_NO_FOOTPRINT $TEST
python3 otter_assign.py $NOTEBOOKS $TEST
python3 jupyterlite_create.py $NOTEBOOKS $OTTER_VERSION $TEST
python3 jupyterlite_create.py $NOTEBOOKS_NO_FOOTPRINT $OTTER_VERSION $TEST
python3 binder_create.py $NOTEBOOKS $OTTER_VERSION $TEST
python3 binder_create.py $NOTEBOOKS_NO_FOOTPRINT $OTTER_VERSION $TEST
mv notebooks notebooks_normal
mv notebooks_clean notebooks
