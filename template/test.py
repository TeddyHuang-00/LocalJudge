import logging
import os
import subprocess
from timeit import Timer

from config import *
from rich.logging import RichHandler

# Get the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(RichHandler())

# Compile the code
logger.debug(f"Compiling {cpp_file_name} using {cpp_standard}...")
subprocess.run(
    [
        "g++",
        f"./{cpp_file_name}",
        f"-std={cpp_standard}",
        "-o",
        f"./{cpp_file_name.split('.')[0]}",
    ]
)

# Collect tests
logger.debug(f"Collecting tests...")
num_tests = len(list(filter(lambda x: x.endswith(".in"), os.listdir("data"))))
logger.debug(f"Collected {num_tests} tests")
if num_tests == 0:
    logger.error("No tests found")
    exit(1)


# Subroutine to run a test
def run_task(idx: int):
    p = subprocess.Popen(
        [f"./{cpp_file_name.split('.')[0]}"],
        stdin=open(f"data/{idx}.in", "r"),
        stdout=open(f"results/{idx}.out", "w"),
    )
    p.wait()


# Run a singleton test to warm up subprocess
# because the first call to Popen is always slower
logger.debug(f"Warming up...")
run_task(1)

# Run the tests
for i in range(num_tests):
    logger.debug(f"Running test {i+1}...")
    t = Timer(lambda: run_task(i + 1))
    elapsed = t.timeit(number=test_repeat) * 1000 / test_repeat
    res = open(f"results/{i+1}.out", "r").read().strip()
    cout = open(f"data/{i+1}.out", "r").read().strip()
    if res == cout:
        logger.info(f"Test {i+1} passed in {elapsed:.3f} milli seconds")
    else:
        logger.error(f"Test {i+1} failed in {elapsed:.3f} milli seconds")
