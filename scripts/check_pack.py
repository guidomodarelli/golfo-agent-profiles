#!/usr/bin/env python3
"""Checks of the golfo content pack, for its CI and for whoever changes it.

1. The catalog: agent-ready-pack.json with its version, its base and its profiles.
2. The skills: each SKILL.md follows the Agent Skills specification.
3. The version: a change to the content bumps the version and declares it in ``changes`` (with --base).
4. The engine: with the agent-ready-setup skill of golfo-kit (--engine), every profile applies in an
   empty repository that takes its content from this commit through ``sources.golfoKit.source``.

Exit codes: 0 everything passed, 1 a check failed, 2 the arguments are wrong.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from console_output import STATE_DONE, STATE_ERROR, STATE_SKIPPED, STATE_WARNING, Console

PACK_CATALOG_FILE_NAME = "agent-ready-pack.json"
PACK_SCHEMA_VERSION = 1
# Where the content lives: what a change to the content touches.
CONTENT_PATHS = ("base/", "stacks/", "profiles/", PACK_CATALOG_FILE_NAME)
SKILL_FILE_NAME = "SKILL.md"
SKILLS_DIRECTORY_NAME = "skills"
# Agent Skills specification: https://agentskills.io/specification
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_SKILL_NAME_LENGTH = 64
MAX_SKILL_DESCRIPTION_LENGTH = 1024
FRONTMATTER_DELIMITER = "---"
BLOCK_SCALAR_INDICATORS = (">", ">-", ">+", "|", "|-", "|+")
SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
# The repository the consumers declare; the check reaches this checkout at that URL.
PACK_URL = "https://github.com/guidomodarelli/golfo-agent-profiles"
ENGINE_CLI_RELATIVE_PATH = os.path.join("scripts", "agent-ready")
ENGINE_TIMEOUT_SECONDS = 600
ERROR_TAIL_LINES = 6
# The fake provider CLIs the engine finds first: the check never starts a real agent.
PROVIDER_CLIS = ("claude", "codex")
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_USAGE = 2


class CheckError(Exception):
    """A check that cannot run at all (a missing file, Git that does not answer)."""


def read_catalog(pack_dir):
    path = os.path.join(pack_dir, PACK_CATALOG_FILE_NAME)
    try:
        with open(path, encoding="utf-8") as file_handle:
            return json.load(file_handle)
    except (OSError, ValueError) as read_error:
        raise CheckError(f"check_pack: could not read {PACK_CATALOG_FILE_NAME}: {read_error}") from read_error


def semver_key(text):
    match = SEMVER_PATTERN.fullmatch(text) if isinstance(text, str) else None
    return tuple(int(part) for part in match.groups()) if match else None


def catalog_problems(pack_dir, catalog):
    """What the engine would reject before writing, said with the field that has it."""
    problems = []
    if catalog.get("schemaVersion") != PACK_SCHEMA_VERSION:
        problems.append(f"{PACK_CATALOG_FILE_NAME}: schemaVersion must be {PACK_SCHEMA_VERSION}")
    if not semver_key(catalog.get("version")):
        problems.append(f"{PACK_CATALOG_FILE_NAME}: version must be a semver version (1.2.3)")
    base = catalog.get("baseAssets")
    if not isinstance(base, str) or not os.path.isfile(os.path.join(pack_dir, base, "agents-template.md")):
        problems.append(f"{PACK_CATALOG_FILE_NAME}: baseAssets must name the directory with agents-template.md")
    profiles = catalog.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        problems.append(f"{PACK_CATALOG_FILE_NAME}: profiles must list at least one profile")
        return problems
    for name, entry in sorted(profiles.items()):
        assets = entry.get("assets") if isinstance(entry, dict) else None
        if assets is not None and not os.path.isdir(os.path.join(pack_dir, assets)):
            problems.append(f"{PACK_CATALOG_FILE_NAME}: the assets of '{name}' ({assets}) are missing")
    return problems


def frontmatter_fields(text):
    """The top-level ``key: value`` fields of a SKILL.md frontmatter, block scalars and quotes included."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIMITER:
        return None
    fields, current_key, block_lines = {}, None, []
    for line in lines[1:]:
        if line.strip() == FRONTMATTER_DELIMITER:
            break
        if current_key and (line.startswith(" ") or not line.strip()):
            block_lines.append(line.strip())
            continue
        if current_key:
            fields[current_key] = " ".join(part for part in block_lines if part)
            current_key, block_lines = None, []
        key, separator, value = line.partition(":")
        if not separator or line.startswith(" "):
            continue
        value = value.strip()
        if value in BLOCK_SCALAR_INDICATORS:
            current_key = key.strip()
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    else:
        return None
    if current_key:
        fields[current_key] = " ".join(part for part in block_lines if part)
    return fields


def skill_files(pack_dir):
    for directory, directory_names, file_names in os.walk(pack_dir):
        directory_names[:] = sorted(name for name in directory_names if not name.startswith("."))
        if SKILL_FILE_NAME in file_names and os.path.basename(os.path.dirname(directory)) == SKILLS_DIRECTORY_NAME:
            yield os.path.join(directory, SKILL_FILE_NAME)


def skill_problems(pack_dir):
    """Each skill has a valid name equal to its directory and a description within the limit."""
    problems = []
    for path in skill_files(pack_dir):
        relative = os.path.relpath(path, pack_dir).replace(os.sep, "/")
        with open(path, encoding="utf-8") as file_handle:
            fields = frontmatter_fields(file_handle.read())
        if fields is None:
            problems.append(f"{relative}: has no frontmatter between --- lines")
            continue
        name, description = fields.get("name", ""), fields.get("description", "")
        directory = os.path.basename(os.path.dirname(path))
        if not SKILL_NAME_PATTERN.fullmatch(name) or len(name) > MAX_SKILL_NAME_LENGTH:
            problems.append(f"{relative}: name '{name}' must be kebab-case and at most {MAX_SKILL_NAME_LENGTH} characters")
        elif name != directory:
            problems.append(f"{relative}: name '{name}' must be equal to its directory '{directory}'")
        if not description:
            problems.append(f"{relative}: description is empty")
        elif len(description) > MAX_SKILL_DESCRIPTION_LENGTH:
            problems.append(f"{relative}: description has {len(description)} characters, more than {MAX_SKILL_DESCRIPTION_LENGTH}")
    return problems


def run_git(pack_dir, arguments):
    completed = subprocess.run(["git", "-C", pack_dir] + arguments, capture_output=True, text=True, encoding="utf-8")
    if completed.returncode != 0:
        raise CheckError(f"check_pack: git {' '.join(arguments)} failed: {completed.stderr.strip()[:300]}")
    return completed.stdout


def version_problems(changed_paths, base_catalog, catalog):
    """A change to the content needs a higher version, declared in ``changes``."""
    if not any(path.startswith(CONTENT_PATHS) for path in changed_paths):
        return []
    base_version, version = (base_catalog or {}).get("version"), catalog.get("version")
    problems = []
    if base_catalog is not None and semver_key(version) and semver_key(base_version) \
            and semver_key(version) <= semver_key(base_version):
        problems.append(f"the content changed, but version {version} is not higher than {base_version} of the base; "
                        "bump it in agent-ready-pack.json")
    declared = [change.get("version") for change in catalog.get("changes", []) if isinstance(change, dict)]
    if version not in declared:
        problems.append(f"changes has no entry for version {version}; add one with its summary")
    return problems


def changed_since(pack_dir, base_ref):
    """The paths this branch changed against ``base_ref`` and the catalog of the base, or None without one."""
    merge_base = run_git(pack_dir, ["merge-base", base_ref, "HEAD"]).strip()
    changed = run_git(pack_dir, ["diff", "--name-only", f"{merge_base}...HEAD"]).split()
    try:
        base_catalog = json.loads(run_git(pack_dir, ["show", f"{merge_base}:{PACK_CATALOG_FILE_NAME}"]))
    except CheckError:
        base_catalog = None
    return changed, base_catalog


def write_fake_clis(bin_dir):
    """Provider CLIs that answer nothing, so the engine never starts a real agent."""
    os.makedirs(bin_dir, exist_ok=True)
    for name in PROVIDER_CLIS:
        path = os.path.join(bin_dir, name)
        with open(path, "w", encoding="utf-8", newline="\n") as file_handle:
            file_handle.write("#!/bin/sh\nexit 0\n")
        os.chmod(path, 0o755)
        if os.name == "nt":
            with open(path + ".cmd", "w", encoding="utf-8", newline="\r\n") as file_handle:
                file_handle.write("@exit /b 0\n")


def engine_environment(work_dir, pack_dir):
    """An environment of its own: a fake HOME and caches, Git that reaches this checkout at PACK_URL."""
    home = os.path.join(work_dir, "home")
    bin_dir = os.path.join(work_dir, "bin")
    os.makedirs(home, exist_ok=True)
    write_fake_clis(bin_dir)
    git_config = os.path.join(work_dir, "gitconfig")
    environment = {key: value for key, value in os.environ.items() if not key.startswith("AGENT_READY_SETUP_")}
    environment.update({
        "HOME": home, "USERPROFILE": home, "XDG_CACHE_HOME": os.path.join(work_dir, "cache"),
        "XDG_CONFIG_HOME": os.path.join(work_dir, "config"), "GIT_CONFIG_GLOBAL": git_config,
        "PATH": bin_dir + os.pathsep + os.environ.get("PATH", ""),
        "AGENT_READY_SETUP_TOOLS": "0", "AGENT_READY_SETUP_MARKETPLACE_UPGRADED": "1",
        "AGENT_READY_SETUP_ACTIVE_PROVIDER": "claude",
        "AGENT_READY_SETUP_ORGANIZATION_CONFIG": os.path.join(work_dir, "organization.json"),
    })
    pack_url = "file:///" + os.path.abspath(pack_dir).replace(os.sep, "/").lstrip("/")
    for key, value in (("user.name", "agent-ready check"), ("user.email", "check@example.invalid"),
                       ("init.defaultBranch", "main"), ("core.autocrlf", "false"), ("protocol.file.allow", "always"),
                       (f"url.{pack_url}.insteadOf", PACK_URL)):
        subprocess.run(["git", "config", "--file", git_config, key, value], check=True)
    for name in PROVIDER_CLIS:
        found = shutil.which(name, path=environment["PATH"])
        if not found or os.path.dirname(os.path.abspath(found)) != os.path.abspath(bin_dir):
            raise CheckError(f"check_pack: the fake {name} CLI is not the first on PATH ({found}); stopping before the "
                             "engine could start a real agent")
    return environment


def apply_problems(engine_dir, pack_dir, catalog, console):
    """Apply each profile in an empty repository that takes the content of HEAD from this checkout."""
    commit = run_git(pack_dir, ["rev-parse", "HEAD"]).strip()
    if run_git(pack_dir, ["status", "--porcelain", "--"] + list(CONTENT_PATHS)).strip():
        console.state(STATE_WARNING, f"uncommitted changes to the content are not checked: the engine reads commit {commit[:12]}")
    cli = os.path.join(engine_dir, ENGINE_CLI_RELATIVE_PATH)
    if not os.path.isfile(cli):
        raise CheckError(f"check_pack: {cli} is not the agent-ready CLI; --engine must point to the agent-ready-setup skill")
    problems = []
    work_dir = tempfile.mkdtemp(prefix="pack-check-")
    try:
        environment = engine_environment(work_dir, pack_dir)
        for name in sorted(catalog.get("profiles", {})):
            project = os.path.join(work_dir, "projects", name)
            os.makedirs(os.path.join(project, ".agents"))
            subprocess.run(["git", "init", "-q", project], check=True, env=environment)
            manifest = {"profiles": [name], "sources": {"golfoKit": {"source": f"git+{PACK_URL}#{commit}"}}}
            with open(os.path.join(project, ".agents", "agent-ready.json"), "w", encoding="utf-8") as file_handle:
                json.dump(manifest, file_handle)
            with console.spinner(f"applying {name}"):
                completed = subprocess.run([sys.executable, cli, "apply"], cwd=project, env=environment, capture_output=True,
                                           text=True, encoding="utf-8", errors="replace", timeout=ENGINE_TIMEOUT_SECONDS)
            if completed.returncode == 0:
                console.state(STATE_DONE, f"{name} applies")
                continue
            tail = " | ".join(completed.stderr.strip().splitlines()[-ERROR_TAIL_LINES:])
            console.state(STATE_ERROR, f"{name} does not apply (exit {completed.returncode})")
            problems.append(f"profile '{name}' does not apply with the engine (exit {completed.returncode}): {tail}")
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)
    return problems


def report(console, problems):
    for problem in problems:
        console.state(STATE_ERROR, problem)
    if not problems:
        console.state(STATE_DONE, "no problems")


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description="Check the golfo content pack: catalog, skills, version and engine.")
    parser.add_argument("--pack", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        help="root of the pack (default: this repository)")
    parser.add_argument("--base", help="Git ref to compare the version with, such as origin/main")
    parser.add_argument("--engine", help="the agent-ready-setup skill of golfo-kit that applies each profile")
    return parser.parse_args(argv)


def main(argv=None, console=None):
    arguments = parse_arguments(argv)
    console = console or Console()
    total = 4
    problems = []
    console.banner("golfo content pack", f"Checking {os.path.abspath(arguments.pack)}")
    try:
        catalog = read_catalog(arguments.pack)
        console.step(1, total, "Catalog")
        found = catalog_problems(arguments.pack, catalog)
        report(console, found)
        problems += found
        console.step(2, total, "Skills")
        found = skill_problems(arguments.pack)
        report(console, found)
        problems += found
        console.step(3, total, "Version")
        if arguments.base:
            changed, base_catalog = changed_since(arguments.pack, arguments.base)
            found = version_problems(changed, base_catalog, catalog)
            report(console, found)
            problems += found
        else:
            console.state(STATE_SKIPPED, "no --base: the version is not compared")
        console.step(4, total, "Projection with the engine")
        if arguments.engine:
            problems += apply_problems(arguments.engine, arguments.pack, catalog, console)
        else:
            console.state(STATE_SKIPPED, "no --engine: the profiles are not applied")
    except (CheckError, subprocess.SubprocessError, OSError) as check_error:
        console.failure(str(check_error))
        return EXIT_FAILURE
    if problems:
        console.summary(f"{len(problems)} problem(s) in the pack", ["Fix them and run it again:",
                        "python3 scripts/check_pack.py --base origin/main --engine <agent-ready-setup>"], False)
        return EXIT_FAILURE
    console.summary("The pack is ready", ["Every check passed."], True)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
