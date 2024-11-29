# SPDX-FileCopyrightText: 2024 Guilherme Leoi
#
# SPDX-License-Identifier: Apache-2.0

import traceback
from enum import IntEnum

import os
import pandas as pd
from zipfile import ZipFile
    
from . import download_liar_dataset


class Status(IntEnum):
    OK = 0
    ERROR = 1


def main() -> Status:
    try:
        if not os.path.isfile("./liar_dataset.zip"):
            download_liar_dataset()
        zipped_dataset = ZipFile("./liar_dataset.zip")
        dataset = {
            zipped_file.filename:
                pd.read_csv(zipped_dataset.open(zipped_file.filename), sep='\t')
            for zipped_file in zipped_dataset.infolist()
            if zipped_file.filename.endswith(".tsv")
        }
        #...
        
        return Status.OK
    except:
        traceback.print_exc()
        return Status.ERROR


if __name__ == "__main__":
    import sys
    sys.exit(main())
