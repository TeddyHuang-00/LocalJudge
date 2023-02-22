import logging
import os
import shutil
import sys
from argparse import ArgumentParser

from rich.logging import RichHandler

# Logger settings
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(RichHandler())

# Get existed problems
dir_list = sorted(
    list(filter(lambda x: os.path.isdir(x) and "-" in x, os.listdir())),
    key=lambda x: int(x.split("-")[0]),
)
logger.debug(f"Found {len(dir_list)} existing problems")

# Parse arguments
argparser = ArgumentParser()
argparser.add_argument(
    "name",
    type=str,
    help="Name of the problem",
    default="New",
)
argparser.add_argument(
    "--index",
    type=int,
    help="Manual index of the problem",
    default=len(dir_list),
)
argparser.add_argument(
    "--template",
    type=str,
    help="Template directory of the problem",
    default="template",
)
argparser.add_argument(
    "--compiler",
    type=str,
    help="Compiler to compile the source code",
    default="g++",
)
argparser.add_argument(
    "--source",
    type=str,
    help="Source code of the solution to the problem",
    default="solution.cpp",
)
argparser.add_argument(
    "--standard",
    type=str,
    help="C++ standard to compile the source code",
    default="c++17",
)
argparser.add_argument(
    "--repeat",
    type=int,
    help="Number of times to repeat the test",
    default=10,
)
args = argparser.parse_args()

# Create problem from template
problem_name = f"{args.index}-{args.name}"
shutil.copytree(args.template, problem_name)
logger.debug(f"Created problem {problem_name}")

# Rename source code if necessary
if args.source != "solution.cpp":
    os.rename(
        os.path.join(problem_name, "solution.cpp"),
        os.path.join(problem_name, args.source),
    )
    logger.debug(f"Renamed solution.cpp to {args.source}")

# Create sub-directories
os.mkdir(os.path.join(problem_name, "data"))
logger.debug(f"Created data sub-directory")

os.mkdir(os.path.join(problem_name, "results"))
logger.debug(f"Created results sub-directory")

# Overwrite config.py
with open(os.path.join(problem_name, "config.py"), "w") as f:
    f.write(f'cpp_compiler = "{args.compiler}"\n')
    f.write(f'cpp_file_name = "{args.source}"\n')
    f.write(f'cpp_standard = "{args.standard}"\n')
    f.write(f"test_repeat = {args.repeat}\n")
logger.debug(f"Overwrote config.py")
