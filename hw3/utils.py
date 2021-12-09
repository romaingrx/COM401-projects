#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux (345081)
@date : 2021 Oct 30, 12:21:25
@last modified : 2021 Dec 09, 14:58:10
"""

import re, sys, ast


def get_values_from_parameters(filename: str, keys: str):
    def get_single_key(key: str):
        with open(filename, "r") as fd:
            raw_text = fd.read()
        z = re.findall(fr"^\s*{key}\s*=\s*(.+)\s*$", raw_text, re.MULTILINE)
        if len(z) != 1:
            if len(z):
                print("Found several matches for key `{key}` : ", z, file=sys.stderr)
            return None
        return ast.literal_eval(z[0])

    if type(keys) == str:
        return get_single_key(keys)
    elif type(keys) in (list, tuple):
        return tuple([get_single_key(key) for key in keys])
    else:
        raise TypeError(
            f"type of keys not understood : {type(keys)}, only accept str, list or tuple"
        )
