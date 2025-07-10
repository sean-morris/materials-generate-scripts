# This script removes Otter Grader cells from Jupyter notebooks. DO NOT RUN IT 
# from here. Copy the repo materials-fds when they are ready to the repo materials-fds-otterless,
# then copy this file into the materials-fds-otterless repo and run it there. Then remove it! 
import os
import json

# Keywords to search for in cell source
KEYWORDS = [
    "grader.check",
    "grader.check_all",
    "grader.export",
    "grader = otter.Notebook"
]


def should_remove(cell):
    if cell["cell_type"] != "code":
        return False
    source = "".join(cell.get("source", []))
    return any(keyword in source for keyword in KEYWORDS)


def process_notebook(path):
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    original_len = len(nb["cells"])
    nb["cells"] = [cell for cell in nb["cells"] if not should_remove(cell)]
    if len(nb["cells"]) < original_len:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1)
        print(f"Updated: {path}")

# READ THIS!
# This script removes Otter Grader cells from Jupyter notebooks. DO NOT RUN IT 
# from here. Copy the repo materials-fds when they are ready to the repo materials-fds-otterless,
# then copy this file into the materials-fds-otterless repo and run it there. Then remove it! 
def main():
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".ipynb"):
                process_notebook(os.path.join(root, file))

if __name__ == "__main__":
    main()