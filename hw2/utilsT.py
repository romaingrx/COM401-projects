
import re, sys
import ast


def get_value_from_parameters(filename: str, key: str):
    with open(filename, "r") as fd:
        raw_text = fd.read()
    z = re.findall(fr"^\s*{key}\s*=\s*(.+)\s*$", raw_text, re.MULTILINE)
    if len(z) != 1:
        if len(z):
            print("Found several matches for key `{key}` : ", z, file=sys.stderr)
        return None
    return ast.literal_eval(z[0].replace("'", '"'))  # TODO: replace?


if __name__ == "__main__":
    import json

    value = get_value_from_parameters("345081-parameters.txt", "Q3_dict")
    print(json.loads(value))