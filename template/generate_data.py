import logging
import os

import numpy as np
from rich.logging import RichHandler

# Get the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(RichHandler())

# Some params of the problem
N = [10, 100, 1_000, 10_000]

for i, n in enumerate(N):
    # Generate problem data
    logger.info(f"Generating case {i+1}...")
    digits = np.random.choice(10, size=(n, 9))
    nums = np.array(
        list(map(lambda x: int("".join(map(str, x))), digits))
    ) * np.random.choice([-1, 1], size=n)
    sums = nums[:, None] + nums[None, :]
    sums *= np.tri(*sums.shape, k=-1, dtype=bool)
    uniq_sums, count = np.unique(sums, return_counts=True)
    target = uniq_sums[np.random.choice(np.where(count == 1)[0])]
    index = np.where(sums == target)

    # Create directory
    if not os.path.exists("data"):
        os.mkdir("data")

    # Write to files
    with open(f"data/{i+1}.in", "w") as f:
        f.write(f"{n} {target}\n")
        f.write(" ".join(map(str, nums)))
    with open(f"data/{i+1}.out", "w") as f:
        f.write(f"{min(*index)[0]} {max(*index)[0]}\n")
    logger.info(f"Case {i+1} done")
