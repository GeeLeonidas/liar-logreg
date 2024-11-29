# SPDX-FileCopyrightText: 2024 Guilherme Leoi
#
# SPDX-License-Identifier: Apache-2.0

CODE_OK = 0
CODE_ERROR = 1


def main() -> int:
    try:
        #...
        
        return CODE_OK
    except:
        return CODE_ERROR


if __name__ == "__main__":
    import sys
    sys.exit(main())
