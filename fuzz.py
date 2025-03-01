from typing import get_type_hints
import typing
import random

# this needs to be generalize, can create a type distribution interface


def gen_input(val_type: type):
    # use get typing.get_origin for nested types

    wrapper_type = typing.get_origin(val_type)
    if wrapper_type is list:
        length = random.randint(0, 10)
        inner_type = typing.get_args(val_type)[0]
        lst = []
        for _ in range(length):
            lst.append(gen_input(inner_type))
        return lst

    # dict and other types exist

    if val_type is int:
        return random.randint(-1000, 1000)

    if val_type is str:
        return ""

    return None


def gen_args(arg_types: dict, n: int) -> list[dict]:
    out = []
    for _ in range(n):
        params = {}
        for k, v in arg_types.items():
            if k == "return":
                continue
            params[k] = gen_input(v)
        out.append(params)
    return out


# take a function, go through all its inputs, and randomly sample parts of the input space
def fuzz(f):
    hints = get_type_hints(f)

    # see if it breaks it
    test_inputs = gen_args(hints, 100)
    # print(test_inputs)
    for x in test_inputs:
        f(**x)
