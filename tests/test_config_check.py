import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/rust-server-toolkit/skills/rust-plugin-config/scripts/config_check.py"
spec = importlib.util.spec_from_file_location("config_check", SCRIPT)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, text):
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return path

    def run_cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = config.main(list(map(str, args)))
        return code, json.loads(output.getvalue())

    def test_bom_unicode_and_no_write(self):
        path = self.write("a.json", '\ufeff{"Description":"Unicode \\u2603","Rate":2.0}')
        before = path.read_bytes()
        code, result = self.run_cli("check", path)
        self.assertEqual(code, 0)
        self.assertTrue(result["valid"])
        self.assertEqual(path.read_bytes(), before)

    def test_duplicate_nested_key_rejected_without_disclosure(self):
        path = self.write("a.json", '{"a":{"private-key":1,"private-key":2}}')
        code, result = self.run_cli("check", path)
        self.assertEqual(code, 2)
        self.assertNotIn("private-key", json.dumps(result))

    def test_invalid_json_and_non_finite(self):
        for text in ('{"x":}', '{"x":1,}', '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}'):
            with self.subTest(text=text):
                code, result = self.run_cli("check", self.write("a.json", text))
                self.assertEqual(code, 2)
                self.assertFalse(result["valid"])

    def test_precise_large_numbers_are_compared(self):
        a = self.write("a.json", '{"x":1e400}')
        b = self.write("b.json", '{"x":2e400}')
        code, result = self.run_cli("diff", a, b)
        self.assertEqual(code, 0)
        self.assertEqual(result["count"], 1)

    def test_diff_types_paths_and_values(self):
        a = self.write("a.json", '{"a/b~c":1,"secret":"old-secret","gone":true,"arr":[true]}')
        b = self.write("b.json", '{"a/b~c":false,"secret":"new-secret","new":[],"arr":[1]}')
        before = (a.read_bytes(), b.read_bytes())
        code, result = self.run_cli("diff", a, b)
        self.assertEqual(code, 0)
        self.assertEqual(result["count"], 5)
        self.assertIn({"kind":"type_changed", "path":"/a~1b~0c"}, result["changes"])
        self.assertIn({"kind":"changed", "path":"/arr"}, result["changes"])
        self.assertNotIn("old-secret", json.dumps(result))
        self.assertNotIn("new-secret", json.dumps(result))
        self.assertEqual((a.read_bytes(), b.read_bytes()), before)

    def test_same_document_and_root_replacement(self):
        self.assertEqual(config.differences({"x":[1]}, {"x":[1]}), [])
        self.assertEqual(config.differences(None, {}), [{"kind":"type_changed", "path":""}])

    def test_bad_encoding_and_missing_file(self):
        path = self.root / "bad.json"
        path.write_bytes(b"\xff\xfe")
        for value in (path, self.root / "missing.json"):
            self.assertEqual(self.run_cli("check", value)[0], 2)

    def test_deep_input_fails_cleanly(self):
        path = self.write("deep.json", "[" * 2000 + "0" + "]" * 2000)
        self.assertEqual(self.run_cli("check", path)[0], 2)


if __name__ == "__main__":
    unittest.main()
