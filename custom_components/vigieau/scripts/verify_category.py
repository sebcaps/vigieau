from pathlib import Path
from os import path
import json
import re
import sys
import itertools

current_dir = path.dirname(__file__)
parent_dir = path.dirname(current_dir)
sys.path.append(".")
sys.path.append(parent_dir)
from custom_components.vigieau.const import SENSOR_DEFINITIONS

MatcherResultFilename = "matcher_by_category.json"


def generate_matcher_by_category(
    inputFileName="full_usage_list.json", outFileName=MatcherResultFilename
):
    inputFile = Path(f"{current_dir}/{inputFileName}")
    with open(inputFile) as f:
        input = f.read()
        data = json.loads(input)

    match = []
    for sensor in SENSOR_DEFINITIONS:
        restriction_list = []
        for restriction in data["restrictions"]:
            for matcher in sensor.matchers:
                if re.search(matcher, restriction["usage"], re.IGNORECASE):
                    restriction_list.append(restriction["usage"])
        match.append({sensor.name: restriction_list})

    newFile = Path(f"{current_dir}/{outFileName}")
    with open(newFile, "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(match))


def duplicate_inside_category(input_filename=MatcherResultFilename, for_test=False):
    inputFile = Path(f"{current_dir}/{input_filename}")
    with open(inputFile) as f:
        input = f.read()
        datas = json.loads(input)
    final_result = []
    for i in range(len(datas)):
        data = datas[i]
        for value in data:
            duplicate = [x for x in data[value] if data[value].count(x) > 1]
        if len(duplicate) >= 1:
            final_result.append({value: duplicate})

    if not for_test:
        print(final_result)
        newFile = Path(f"{current_dir}/duplicate_by_category.json")
        with open(newFile, "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(final_result))
    return final_result


def duplicate_between_categories(input_filename=MatcherResultFilename, for_test=False):
    inputFile = Path(f"{current_dir}/{input_filename}")
    with open(inputFile) as f:
        input = f.read()
        datas = json.loads(input)
    final_result = []
    for (
        cat1,
        cat2,
    ) in itertools.combinations(
        datas, 2
    ):  # Create all combination between category, so that we can compare them.
        result = compare_cat(cat1, cat2)
        if result:
            final_result.append(result)
    if not for_test:
        print(final_result)
        newFile = Path(f"{current_dir}/duplicate_between_categories.json")
        with open(newFile, "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(final_result))
    return final_result


def compare_cat(cat1: dict, cat2: dict):
    values1 = []
    values2 = []
    for val1 in cat1:  # Extract data from 1st category
        for value in cat1[val1]:
            values1.append(value)
    for val2 in cat2:  # Extract data from 2nd category
        for value in cat2[val2]:
            values2.append(value)

    # print([val1 for val1 in values1 if val1 in values2])
    dupvalues = [
        val1 for val1 in values1 if val1 in values2
    ]  # check if val from st exist in values from 2nd cat

    return {val: [val1, val2] for val in dupvalues}  # Return result


if __name__ == "__main__":
    generate_matcher_by_category()
    duplicate_inside_category()
    duplicate_between_categories()
