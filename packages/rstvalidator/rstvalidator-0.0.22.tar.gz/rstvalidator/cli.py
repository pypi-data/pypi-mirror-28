#!/usr/bin/env python
import sys
from __init__ import rstvalidator

usage = "usage: python -m rstvalidator.cli path ..."

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1 or (len(argv) == 2 and argv[1] == "--help"):
        print(usage)
    else:
        for path in argv[1:]:
            reports = rstvalidator(path)
            if reports:
                print(path)
                print("\n".join(reports))
                sys.exit(1)

