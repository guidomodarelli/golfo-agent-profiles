"""Tests of the checks of the pack and of their output, without the engine and without animation."""

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import check_pack  # noqa: E402
import console_output  # noqa: E402

PACK_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TerminalStream(io.StringIO):
    """A stream that says it is a terminal, for the coloured mode."""

    def isatty(self):
        return True


def write_skill(root, relative_directory, frontmatter):
    directory = os.path.join(root, *relative_directory.split("/"))
    os.makedirs(directory)
    with open(os.path.join(directory, "SKILL.md"), "w", encoding="utf-8") as file_handle:
        file_handle.write(frontmatter)


class FrontmatterTest(unittest.TestCase):
    def test_reads_plain_quoted_and_folded_fields(self):
        fields = check_pack.frontmatter_fields(
            "---\nname: logger\ndescription: >-\n  Crea el logger\n  compartido.\nlicense: \"MIT\"\n---\n# Body\n")
        self.assertEqual(fields, {"name": "logger", "description": "Crea el logger compartido.", "license": "MIT"})

    def test_a_file_without_a_closed_frontmatter_has_none(self):
        self.assertIsNone(check_pack.frontmatter_fields("# Only a body\n"))
        self.assertIsNone(check_pack.frontmatter_fields("---\nname: open\n"))


class SkillProblemsTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root)

    def test_a_valid_skill_has_no_problems(self):
        write_skill(self.root, "stacks/node/skills/logger", "---\nname: logger\ndescription: Crea el logger.\n---\n")
        self.assertEqual(check_pack.skill_problems(self.root), [])

    def test_a_name_unlike_its_directory_and_an_empty_description_are_reported(self):
        write_skill(self.root, "stacks/node/skills/logger", "---\nname: log\ndescription:\n---\n")
        problems = check_pack.skill_problems(self.root)
        self.assertEqual(len(problems), 2)
        self.assertIn("must be equal to its directory 'logger'", problems[0])
        self.assertIn("description is empty", problems[1])

    def test_a_description_over_the_limit_is_reported(self):
        long_description = "x" * (check_pack.MAX_SKILL_DESCRIPTION_LENGTH + 1)
        write_skill(self.root, "base/skills/agent-browser", f"---\nname: agent-browser\ndescription: {long_description}\n---\n")
        self.assertIn("more than 1024", check_pack.skill_problems(self.root)[0])

    def test_a_skill_without_evals_is_listed(self):
        write_skill(self.root, "stacks/react/skills/karpathy-guidelines", "---\nname: karpathy-guidelines\ndescription: d\n---\n")
        write_skill(self.root, "stacks/react/skills/component-creation", "---\nname: component-creation\ndescription: d\n---\n")
        os.makedirs(os.path.join(self.root, "stacks", "react", "skills", "component-creation", "evals"))
        open(os.path.join(self.root, "stacks", "react", "skills", "component-creation", "evals", "eval-config.json"), "w").close()
        self.assertEqual(check_pack.skills_without_evals(self.root), ["stacks/react/skills/karpathy-guidelines"])

    def test_the_skills_of_this_pack_follow_the_specification(self):
        self.assertEqual(check_pack.skill_problems(PACK_ROOT), [])


class VersionProblemsTest(unittest.TestCase):
    def catalog(self, version, changes=()):
        return {"version": version, "changes": [{"version": change, "summary": "s"} for change in changes]}

    def test_a_change_outside_the_content_needs_no_version(self):
        self.assertEqual(check_pack.version_problems(["README.md"], self.catalog("1.0.0"), self.catalog("1.0.0")), [])

    def test_a_change_to_the_content_needs_a_higher_declared_version(self):
        problems = check_pack.version_problems(["stacks/node/rules/x.md"], self.catalog("1.0.0", ["1.0.0"]),
                                               self.catalog("1.0.0", ["1.0.0"]))
        self.assertEqual(len(problems), 1)
        self.assertIn("is not higher than 1.0.0", problems[0])
        problems = check_pack.version_problems(["stacks/node/rules/x.md"], self.catalog("1.0.0", ["1.0.0"]),
                                               self.catalog("1.1.0", ["1.0.0"]))
        self.assertEqual(problems, ["changes has no entry for version 1.1.0; add one with its summary"])
        self.assertEqual(check_pack.version_problems(["stacks/node/rules/x.md"], self.catalog("1.0.0", ["1.0.0"]),
                                                     self.catalog("1.1.0", ["1.1.0", "1.0.0"])), [])

    def test_the_first_version_only_needs_its_changes_entry(self):
        self.assertEqual(check_pack.version_problems([check_pack.PACK_CATALOG_FILE_NAME], None,
                                                     self.catalog("1.0.0", ["1.0.0"])), [])


class CatalogProblemsTest(unittest.TestCase):
    def test_the_catalog_of_this_pack_is_valid(self):
        self.assertEqual(check_pack.catalog_problems(PACK_ROOT, check_pack.read_catalog(PACK_ROOT)), [])

    def test_missing_assets_and_template_are_reported(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        problems = check_pack.catalog_problems(root, {"schemaVersion": 1, "version": "1", "baseAssets": "base",
                                                      "profiles": {"node": {"assets": "stacks/node"}}})
        self.assertEqual(len(problems), 3)


class ConsoleTest(unittest.TestCase):
    def test_plain_mode_has_no_escapes_and_the_spinner_does_not_animate(self):
        stream = io.StringIO()
        console = console_output.Console(stream=stream)
        self.assertFalse(console.color)
        console.step(1, 2, "Catalog")
        with console.spinner("applying node"):
            pass
        console.state(console_output.STATE_ERROR, "broken")
        console.summary("1 problem", ["Fix it"], False)
        output = stream.getvalue()
        self.assertNotIn("\033", output)
        self.assertIn("[1/2] Catalog", output)
        self.assertIn("... applying node", output)
        self.assertIn("[xx] broken", output)

    def test_colour_mode_paints_and_always_clears_the_spinner_line(self):
        stream = TerminalStream()
        console = console_output.Console(stream=stream, color=True, spinner_interval=0)
        with self.assertRaises(RuntimeError):
            with console.spinner("applying node"):
                raise RuntimeError("the step failed")
        console.state(console_output.STATE_DONE, "fine")
        output = stream.getvalue()
        self.assertTrue(output.endswith("\n"))
        self.assertIn(console_output.ANSI_SHOW_CURSOR, output)
        self.assertIn(console_output.ANSI_GREEN, output)

    def test_no_color_turns_colour_off_even_in_a_terminal(self):
        self.assertFalse(console_output.supports_color(TerminalStream(), {"NO_COLOR": "1"}))
        self.assertFalse(console_output.supports_color(TerminalStream(), {"TERM": "dumb"}))


class MainTest(unittest.TestCase):
    def test_a_pack_with_a_broken_skill_exits_with_one(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        shutil.copy2(os.path.join(PACK_ROOT, check_pack.PACK_CATALOG_FILE_NAME), root)
        catalog = check_pack.read_catalog(root)
        for name, entry in catalog["profiles"].items():
            if "assets" in entry:
                os.makedirs(os.path.join(root, entry["assets"]), exist_ok=True)
        os.makedirs(os.path.join(root, catalog["baseAssets"]), exist_ok=True)
        open(os.path.join(root, catalog["baseAssets"], "agents-template.md"), "w").close()
        write_skill(root, "base/skills/agent-browser", "---\nname: browser\ndescription: d\n---\n")
        stream = io.StringIO()
        status = check_pack.main(["--pack", root], console_output.Console(stream=stream))
        self.assertEqual(status, check_pack.EXIT_FAILURE)
        self.assertIn("1 problem(s) in the pack", stream.getvalue())

    def test_this_pack_passes_without_the_engine(self):
        stream = io.StringIO()
        self.assertEqual(check_pack.main(["--pack", PACK_ROOT], console_output.Console(stream=stream)), check_pack.EXIT_SUCCESS)
        self.assertIn("no --engine", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
