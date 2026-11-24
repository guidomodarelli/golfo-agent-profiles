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

    def test_an_unquoted_colon_space_is_reported_and_a_quoted_one_is_not(self):
        write_skill(self.root, "stacks/node/skills/widgets", "---\nname: widgets\ndescription: Create widgets: use templates\n---\n")
        write_skill(self.root, "stacks/node/skills/quoted", "---\nname: quoted\ndescription: \"Create widgets: use templates\"\n---\n")
        problems = check_pack.skill_problems(self.root)
        self.assertEqual(len(problems), 1)
        self.assertIn("widgets/SKILL.md: description has ': ' without quotes", problems[0])

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

    def test_a_change_to_evals_only_needs_no_version(self):
        evals = ["stacks/nextjs/evals/eval-config.json", "stacks/react/skills/component-creation/evals/eval-config.json"]
        self.assertEqual(check_pack.version_problems(evals, self.catalog("1.0.0", ["1.0.0"]),
                                                     self.catalog("1.0.0", ["1.0.0"])), [])

    def test_evals_next_to_a_content_change_still_need_a_version(self):
        problems = check_pack.version_problems(["stacks/nextjs/evals/eval-config.json", "stacks/nextjs/rules/x.md"],
                                               self.catalog("1.0.0", ["1.0.0"]), self.catalog("1.0.0", ["1.0.0"]))
        self.assertEqual(len(problems), 1)
        self.assertIn("is not higher than 1.0.0", problems[0])

    def test_a_rule_named_like_the_evals_directory_is_still_content(self):
        problems = check_pack.version_problems(["stacks/nextjs/rules/evals"], self.catalog("1.0.0", ["1.0.0"]),
                                               self.catalog("1.0.0", ["1.0.0"]))
        self.assertEqual(len(problems), 1)

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


class ApplyProblemsTest(unittest.TestCase):
    def test_a_relative_engine_path_works_from_the_temporary_repositories(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        # An engine whose CLI only succeeds: what is checked is that it is found.
        os.makedirs(os.path.join(root, "engine", "scripts"))
        with open(os.path.join(root, "engine", "scripts", "agent-ready"), "w", encoding="utf-8") as file_handle:
            file_handle.write("import sys\nsys.exit(0)\n")
        previous = os.getcwd()
        os.chdir(root)
        self.addCleanup(os.chdir, previous)
        console = console_output.Console(stream=io.StringIO())
        problems = check_pack.apply_problems("engine", PACK_ROOT, {"profiles": {"node": {}}}, console)
        self.assertEqual(problems, [])


def write_rule(root, relative_path, text):
    path = os.path.join(root, relative_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as rule_file:
        rule_file.write(text)


class RuleTriggerTest(unittest.TestCase):
    def test_a_rule_with_a_valid_trigger_has_no_problems(self):
        with tempfile.TemporaryDirectory() as root:
            write_rule(root, "base/rules/always.md", "---\ntrigger: always_on\n---\n\n# Always\n")
            write_rule(root, "stacks/node/rules/glob.md", '---\ntrigger: glob\nglobs: "*.ts, *.tsx"\n---\n# Glob\n')
            self.assertEqual(check_pack.rule_trigger_problems(root), [])

    def test_a_rule_without_a_trigger_or_with_an_unknown_one_is_reported(self):
        with tempfile.TemporaryDirectory() as root:
            write_rule(root, "base/rules/plain.md", "# No frontmatter\n")
            write_rule(root, "profiles/acme/rules/camel.md", "---\ntrigger: alwaysOn\n---\n# Camel\n")
            problems = check_pack.rule_trigger_problems(root)
        self.assertEqual(len(problems), 2)
        self.assertIn("base/rules/plain.md: has no trigger", problems[0])
        self.assertIn("profiles/acme/rules/camel.md: has trigger 'alwaysOn'", problems[1])

    def test_glob_and_model_decision_need_their_fields(self):
        with tempfile.TemporaryDirectory() as root:
            write_rule(root, "base/rules/glob.md", "---\ntrigger: glob\n---\n# Glob\n")
            write_rule(root, "base/rules/decision.md", "---\ntrigger: model_decision\n---\n# Decision\n")
            problems = check_pack.rule_trigger_problems(root)
        self.assertTrue(any("decision.md: trigger model_decision needs a description" in problem for problem in problems))
        self.assertTrue(any("glob.md: trigger glob needs globs" in problem for problem in problems))

    def test_the_evals_of_the_rules_are_not_rules(self):
        with tempfile.TemporaryDirectory() as root:
            write_rule(root, "stacks/node/rules/evals/notes.md", "# Not a rule\n")
            self.assertEqual(check_pack.rule_trigger_problems(root), [])

    def test_the_rules_of_this_pack_declare_their_trigger(self):
        self.assertEqual(check_pack.rule_trigger_problems(PACK_ROOT), [])


def write_fake_engine(root, lint_result):
    """An engine whose CLI answers agent-ready rules lint with ``lint_result`` as its JSON."""
    os.makedirs(os.path.join(root, "engine", "scripts"))
    with open(os.path.join(root, "engine", "scripts", "agent-ready"), "w", encoding="utf-8") as file_handle:
        file_handle.write("import json, sys\nprint(json.dumps(%r))\nsys.exit(1 if %r else 0)\n"
                          % (lint_result, any(finding["level"] == "error" for finding in lint_result["findings"])))
    return os.path.join(root, "engine")


class RuleProblemsTest(unittest.TestCase):
    def test_each_lint_error_is_a_problem_and_a_warning_is_not(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        engine = write_fake_engine(root, {"rules": 2, "errors": 1, "warnings": 1, "findings": [
            {"level": "error", "code": "untagged-rule", "path": "stacks/node/rules/node-testing.md", "line": 4,
             "rule": None, "message": "a top-level bullet without a marker"},
            {"level": "warning", "code": "statement-long", "path": "base/rules/verify-changes.md", "line": 9,
             "rule": "verify-changes/report", "message": "the statement is long"}]})
        stream = io.StringIO()
        problems = check_pack.rule_problems(engine, PACK_ROOT, console_output.Console(stream=stream))
        self.assertEqual(problems, ["stacks/node/rules/node-testing.md:4: [untagged-rule]: a top-level bullet without a marker"])
        self.assertIn("1 warning(s) of agent-ready rules lint", stream.getvalue())

    def test_a_pack_without_lint_errors_has_no_problems(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        engine = write_fake_engine(root, {"rules": 3, "errors": 0, "warnings": 0, "findings": []})
        stream = io.StringIO()
        self.assertEqual(check_pack.rule_problems(engine, PACK_ROOT, console_output.Console(stream=stream)), [])
        self.assertIn("3 atomic rules, no lint error", stream.getvalue())

    def test_an_engine_that_gives_no_json_stops_the_check(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        os.makedirs(os.path.join(root, "engine", "scripts"))
        with open(os.path.join(root, "engine", "scripts", "agent-ready"), "w", encoding="utf-8") as file_handle:
            file_handle.write("import sys\nsys.stderr.write('unknown command rules\\n')\nsys.exit(2)\n")
        with self.assertRaises(check_pack.CheckError):
            check_pack.rule_problems(os.path.join(root, "engine"), PACK_ROOT, console_output.Console(stream=io.StringIO()))


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
