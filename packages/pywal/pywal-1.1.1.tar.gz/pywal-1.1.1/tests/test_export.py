"""Test export functions."""
import unittest
import unittest.mock
import io
import shutil
import os

from pywal import export
from pywal import util


COLORS = util.read_file_json("tests/test_files/test_file.json")
COLORS["colors"].update(COLORS["special"])

TMP_DIR = "/tmp/wal"


class TestExportColors(unittest.TestCase):
    """Test the export functions."""

    def setUp(self):
        """> Setup export tests."""
        util.create_dir(TMP_DIR)

    def tearDown(self):
        """> Clean up export tests."""
        shutil.rmtree(TMP_DIR, ignore_errors=True)

    def is_file(self, tmp_file):
        """> Test is something is a file."""
        result = os.path.isfile(tmp_file)
        self.assertTrue(result)

    def is_file_contents(self, tmp_file, pattern):
        """> Check for pattern in file."""
        content = util.read_file(tmp_file)
        self.assertEqual(content[6], pattern)

    def test_all_templates(self):
        """> Test substitutions in template file."""
        tmp_file = os.path.join(TMP_DIR, "colors.sh")
        export.every(COLORS, TMP_DIR)

        self.is_file(tmp_file)
        self.is_file_contents(tmp_file, "foreground='#F5F1F4'")

    def test_css_template(self):
        """> Test substitutions in template file (css)."""
        tmp_file = os.path.join(TMP_DIR, "test.css")
        export.color(COLORS, "css", tmp_file)

        self.is_file(tmp_file)
        self.is_file_contents(tmp_file, "    --background: #1F211E;")


class TestInvalidExport(unittest.TestCase):
    """Test export function error handling."""

    def test_invalid_template(self):
        """> Test template validation."""
        error_msg = "warning: template 'dummy' doesn't exist."
        tmp_file = os.path.join(TMP_DIR, "test.css")

        # Since this function prints a message on fail we redirect
        # it's output so that we can read it.
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            export.color(COLORS, "dummy", tmp_file)
            self.assertEqual(fake_out.getvalue().strip(), error_msg)


if __name__ == "__main__":
    unittest.main()
