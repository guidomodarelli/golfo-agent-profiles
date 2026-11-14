#!/usr/bin/env python3
"""Publish the version of agent-ready-pack.json as tag v<version> with a GitHub release, once.

The release notes are the ``changes`` entry of that version. A version that already has its tag is
skipped: a published tag never moves, because consumers pin it.

Exit codes: 0 published or already published, 1 the release failed.
"""

import os
import subprocess
import sys

from check_pack import PACK_CATALOG_FILE_NAME, CheckError, read_catalog, semver_key
from console_output import STATE_DONE, STATE_SKIPPED, Console

TAG_PREFIX = "v"
BREAKING_LABEL = "**Breaking:**"
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def release_notes(catalog):
    """The notes of the current version: its summary, marked when it breaks something."""
    version = catalog["version"]
    for change in catalog.get("changes", []):
        if isinstance(change, dict) and change.get("version") == version:
            summary = change.get("summary", "").strip()
            return f"{BREAKING_LABEL} {summary}" if change.get("breaking") else summary
    raise CheckError(f"release: {PACK_CATALOG_FILE_NAME} has no changes entry for version {version}")


def tag_exists(tag):
    completed = subprocess.run(["git", "ls-remote", "--tags", "origin", f"refs/tags/{tag}"], capture_output=True, text=True)
    if completed.returncode != 0:
        raise CheckError(f"release: git ls-remote origin failed: {completed.stderr.strip()[:300]}")
    return bool(completed.stdout.strip())


def main(console=None):
    console = console or Console()
    pack_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    console.banner("golfo content pack", "Publishing the version of agent-ready-pack.json")
    try:
        catalog = read_catalog(pack_dir)
        if not semver_key(catalog.get("version")):
            raise CheckError(f"release: version '{catalog.get('version')}' of {PACK_CATALOG_FILE_NAME} is not semver")
        tag = TAG_PREFIX + catalog["version"]
        console.step(1, 2, f"Tag {tag}")
        if tag_exists(tag):
            console.state(STATE_SKIPPED, f"{tag} is already published")
            console.summary(f"{tag} was already published", ["Nothing to do."], True)
            return EXIT_SUCCESS
        notes = release_notes(catalog)
        console.step(2, 2, f"Release {tag}")
        target = os.environ.get("GITHUB_SHA") or subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                                                                  text=True, check=True).stdout.strip()
        with console.spinner(f"creating {tag}"):
            completed = subprocess.run(["gh", "release", "create", tag, "--target", target, "--title", tag, "--notes", notes],
                                       capture_output=True, text=True)
        if completed.returncode != 0:
            raise CheckError(f"release: gh release create {tag} failed: {completed.stderr.strip()[:300]}")
        console.state(STATE_DONE, f"{tag} published at {target[:12]}")
    except (CheckError, OSError, subprocess.SubprocessError) as release_error:
        console.failure(str(release_error))
        return EXIT_FAILURE
    console.summary(f"{tag} is published", [f"Consumers adopt it with ref {tag}, or follow main."], True)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
