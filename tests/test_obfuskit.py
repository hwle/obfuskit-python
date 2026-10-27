import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from obfuskit import obfuscate

class ObfusKitTests(unittest.TestCase):
    def test_renames_names_and_compiles(self):
        source = "def hello(person):\n    message = 'hi'\n    return message + person\n"
        transformed, mapping = obfuscate(source)
        compile(transformed, "<transformed>", "exec")
        self.assertNotIn('"person"', transformed)
        self.assertIn("_v", transformed)
        self.assertTrue(mapping)

    def test_keep_list(self):
        source = "def public_api(value):\n    return value\n"
        transformed, _ = obfuscate(source, {"public_api", "value"})
        self.assertIn("public_api", transformed)
        self.assertIn("value", transformed)

if __name__ == "__main__":
    unittest.main()
