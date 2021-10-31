#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux (345081) & Thomas Benchetrit (284001)
@date : 2021 Oct 30, 12:21:25
@last modified : 2021 Oct 31, 21:30:39
"""

import re, sys, ast


def get_value_from_parameters(filename: str, key: str):
    with open(filename, "r") as fd:
        raw_text = fd.read()
    z = re.findall(fr"^\s*{key}\s*=\s*(.+)\s*$", raw_text, re.MULTILINE)
    if len(z) != 1:
        if len(z):
            print("Found several matches for key `{key}` : ", z, file=sys.stderr)
        return None
    return ast.literal_eval(z[0])
