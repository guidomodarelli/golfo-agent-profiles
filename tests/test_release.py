"""Tests of the release notes, without Git or GitHub."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import check_pack  # noqa: E402
import release  # noqa: E402


class ReleaseNotesTest(unittest.TestCase):
    def test_the_notes_are_the_summary_of_the_current_version(self):
        catalog = {"version": "1.1.0", "changes": [{"version": "1.1.0", "summary": "Rule nueva"},
                                                   {"version": "1.0.0", "summary": "Primera"}]}
        self.assertEqual(release.release_notes(catalog), "Rule nueva")

    def test_a_breaking_change_is_marked(self):
        catalog = {"version": "2.0.0", "changes": [{"version": "2.0.0", "summary": "Sin java", "breaking": True}]}
        self.assertEqual(release.release_notes(catalog), "**Breaking:** Sin java")

    def test_a_version_without_its_entry_stops_the_release(self):
        with self.assertRaises(check_pack.CheckError):
            release.release_notes({"version": "1.2.0", "changes": []})


if __name__ == "__main__":
    unittest.main()
