OTTER_VERSION=4.4.1
COLAB_CLONE_REPO=https://github.com/data-8
COLAB_REPO_MATERIALS=materials-sp22-colab
NOTEBOOKS=notebooks
NOTEBOOKS_NO_FOOTPRINT=notebooks_no_footprint
ASSETS_URL=https://ds-modules.github.io/materials-sp22-assets
TEST_NOTEBOOK=hw03.ipynb
TEST=--is_test  # --is_test or --no-is_test - if set to is-test -- it will only do one notebook of each
RUN_OTTER_TESTS=--run_otter_tests  # --run_otter_tests or --no-run_otter_tests - if set to run_otter_tests -- it will run autograder tests for each notebook and confirm all pass

rm -rf $NOTEBOOKS
rm -rf notebooks_assets
cp -r _${NOTEBOOKS}_raw ${NOTEBOOKS}
python3 colab_notebooks.py $NOTEBOOKS $OTTER_VERSION $COLAB_CLONE_REPO $COLAB_REPO_MATERIALS $TEST $RUN_OTTER_TESTS $TEST_NOTEBOOK
python3 copy_to_assets.py $NOTEBOOKS $TEST $TEST_NOTEBOOK
python3 modify_notebooks_file_access.py $NOTEBOOKS_NO_FOOTPRINT $ASSETS_URL $TEST $TEST_NOTEBOOK
python3 colab_notebooks.py $NOTEBOOKS_NO_FOOTPRINT $OTTER_VERSION $COLAB_CLONE_REPO $COLAB_REPO_MATERIALS $TEST $RUN_OTTER_TESTS $TEST_NOTEBOOK
#python3 otter_assign.py $NOTEBOOKS_NO_FOOTPRINT $TEST $TEST_NOTEBOOK
#python3 otter_assign.py $NOTEBOOKS $TEST $TEST_NOTEBOOK
#python3 jupyterlite_create.py $NOTEBOOKS $OTTER_VERSION $TEST $TEST_NOTEBOOK
# python3 jupyterlite_create.py $NOTEBOOKS_NO_FOOTPRINT $OTTER_VERSION $TEST $TEST_NOTEBOOK
#python3 binder_create.py $NOTEBOOKS $OTTER_VERSION $TEST $TEST_NOTEBOOK
# python3 binder_create.py $NOTEBOOKS_NO_FOOTPRINT $OTTER_VERSION $TEST $TEST_NOTEBOOK


