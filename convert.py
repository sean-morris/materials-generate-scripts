from subprocess import run
import os
import argparse
import sys


def convert(name, path):
    '''
        @param single_file if you want to process one file or path
    '''
    with open("./logs.txt", "w") as log:
        log.write(f"Logs for {name} at {path}")
    with open("./logs.txt", "a") as log:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".ipynb") and "checkpoints" not in root:
                    file_path = os.path.join(root, file)
                    new_file_path = os.path.join(name + "/" + root, file)
                    os.makedirs("./" + name + "/" + root, exist_ok=True)
                    print("Processing file:", file_path)
                    convert_out = run(["python3", "-m", "otter.assign.v0.convert", file_path, new_file_path], capture_output=True,  encoding='utf8')
                    if convert_out.returncode == 0:
                        log.write(f"Converted: {file_path} \n")
                    else:
                        log.write(f"ERROR at {file_path}:\n")
                        for line in convert_out.stderr.splitlines():
                            log.write(f"{line} \n")

    print("Finished: Logs at ./logs.txt")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert the notebooks in path from v0 to v1')
    parser.add_argument('name', metavar='n', type=str, help='the new name used to make path')
    parser.add_argument('path', metavar='n', type=str, help='the path to use to find notebooks')
    args, unknown = parser.parse_known_args()
    u = convert(args.name, args.path)
    sys.exit(u)
