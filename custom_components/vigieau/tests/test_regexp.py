from os import path
import sys

current_dir = path.dirname(__file__)
parent_dir = path.dirname(current_dir)
sys.path.append(".")
sys.path.append(parent_dir)
from custom_components.vigieau.const import SENSOR_DEFINITIONS
from custom_components.vigieau.scripts.verify_category import (
    duplicate_inside_category,
    duplicate_between_categories,
    generate_matcher_by_category,
)
import unittest
from pathlib import Path
import json
import re


class TestRegexp(unittest.TestCase):
    def test_matcher_in_component(self):
        # Open file with as many usage as possible ;-)
        file = Path(f"{parent_dir}/scripts/full_usage_list.json")
        with open(file) as f:
            input = f.read()
        data = json.loads(input)

        for restriction in data["restrictions"]:  # For all restrictions in the list
            with self.subTest(
                msg="One matcher failed"
            ):  # For soft fail, ref https://stackoverflow.com/questions/4732827/continuing-in-pythons-unittest-when-an-assertion-fails
                found = False
                for (
                    sensor
                ) in (
                    SENSOR_DEFINITIONS
                ):  # We may have to create a function rather than copy/paste, but it's a 'simple re.search....
                    for matcher in sensor.matchers:
                        if re.search(
                            matcher,
                            restriction["usage"],
                            re.IGNORECASE,
                        ):
                            found = True
                self.assertTrue(
                    found,
                    f"Value **{restriction['usage']}** in category **{restriction['thematique']}** not found in matcher",
                )  # Check for one usage if it has been found


class TestResult(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        generate_matcher_by_category()

    def test_duplicateInCategory(self):
        result = duplicate_inside_category(for_test=True)
        self.assertEqual(
            len(result), 0, "Il y a des duplicats  à l'interieur d'une catégorie"
        )

    def test_duplicatebetweenCategory(self):
        result = duplicate_between_categories(for_test=True)
        self.assertEqual(len(result), 0, "Il y a des duplicats entre les catégories")


if __name__ == "__main__":
    unittest.main()
