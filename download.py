# SPDX-FileCopyrightText: 2024 Guilherme Leoi
#
# SPDX-License-Identifier: Apache-2.0

import urllib.request


def __download_file(url: str, target_path: str):
    dataset_file = urllib.request.urlopen(url)
    with open(target_path, "wb") as output:
        output.write(dataset_file.read())


def download_liar_dataset():
    notice = """
===================================================================
NOTICE FROM THE LIAR DATASET
===================================================================
The original sources retain the copyright of the data.

Note that there are absolutely no guarantees with this data,
and we provide this dataset "as is",
but you are welcome to report the issues of the preliminary version
of this data.

You are allowed to use this dataset for research purposes only.

For more question about the dataset, please contact:
William Wang, william@cs.ucsb.edu
===================================================================
"""[1:-2]
    print(notice)
    __download_file(
        url = "https://sites.cs.ucsb.edu/~william/data/liar_dataset.zip",
        target_path = "./liar_dataset.zip",
    )


if __name__ == "__main__":
    download_liar_dataset()
