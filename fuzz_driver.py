import importlib
import fuzz
import sys

if "__main__" == __name__:
    lib_name = sys.argv[1]
    lib_name = lib_name.split(".")[0]  # remove extension
    lib_name = lib_name.replace("/", ".")
    lib = importlib.import_module(lib_name)
    for name in dir(lib):
        if name.startswith("__"):
            continue
        if name == "deal":
            continue
        fuzz.fuzz(getattr(lib, name))

