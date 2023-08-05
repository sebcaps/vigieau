import unittest
from pathlib import Path
import json
import re

from custom_components.vigieau.const import SENSOR_DEFINITIONS


class Test(unittest.TestCase):
    def test_matcher(self):

        # FIXME handle relative path
        # Open file with as many usage as possible ;-)
        file = Path("/workspaces/vigieau/custom_components/vigieau/tests/usage_list.json")
        with open(file) as f:
            input = f.read()
        data = json.loads(input)

        for usage in data['usages']: #For all usages in the list
            print (usage)
            with self.subTest(msg='One matcher failed'): # For soft fail, ref https://stackoverflow.com/questions/4732827/continuing-in-pythons-unittest-when-an-assertion-fails
                found = False
                for sensor in SENSOR_DEFINITIONS: # We may have to create a function rather than copy/paste, but it's a 'simple re.search....
                    for matcher in sensor.matchers:
                        if re.search(matcher,usage,re.IGNORECASE,):
                            found = True
                self.assertTrue(found,f"Value {usage} not found in matcher") #Check for one usage if it has been found


if __name__ == "__main__":
    unittest.main()
