"""Sync thesis/ with the TUM Overleaf project, without ever losing prose.

The problem this exists to prevent
-----------------------------------
Overleaf's git server PROHIBITS force pushes, and `git subtree pull/push` does
not work here because `thesis/` was created by an ordinary commit rather than
by `git subtree add`. The remaining technique -- build a commit whose parent is
Overleaf's head and fast-forward onto it -- replaces the remote tree WHOLESALE.

That is safe onto an empty project and catastrophic onto one with writing in it:
the push is a valid fast-forward, so git raises no conflict, prints no warning,
and the prose is simply gone. Nobody finds out until they open the editor.

So the push here REFUSES when Overleaf holds writing that is not in the local
`thesis/`, and says exactly which files. `--overwrite` is the only way past it,
and must be typed deliberately.

How it tells an update from a divergence
----------------------------------------
The first version of this script compared the two trees file by file and
treated ANY differing file as a reason to refuse. That was wrong, and wrong in
the direction that destroys the guard: a differing file is what a normal update
looks like, so every push after the first demanded `--overwrite`. A flag typed
every time is a flag that has stopped meaning anything, and the one push where
Overleaf really did hold your browser edits would have been waved through out
of habit.

The distinction the comparison was missing is provenance, not content. Every
tree this script pushes is `thesis/` at some commit of ours, so:

  - if the remote tree EQUALS `<commit>:thesis` for any commit in this repo's
    history, then the remote holds nothing that did not come from here. It is
    an older state of your own work, the push is a plain forward update, and no
    flag is required no matter how many files differ.
  - if the remote tree matches NO commit of ours, someone wrote on Overleaf.
    That is the case `--overwrite` exists for, and it still refuses without it.

`find_remote_tree_in_history()` is that check. Deletions are reported loudly
even on a recognised remote, because "this file is on Overleaf and not here"
reads the same whether you deleted it deliberately or never had it.

What it will not do
-------------------
- never `--force`, never rewrite history: the pushed commit always descends
  from the current remote head, so a fast-forward is the only thing attempted.
- never auto-commit a pull. Overleaf's files land as ordinary working-tree
  changes for you to read in `git diff` and commit yourself.
- never delete a local file that Overleaf lacks. It is reported, not removed.
- no default action. Bare invocation compares and prints; nothing is written.

Usage
-----
    python scripts/sync_overleaf.py              # status only, writes nothing
    python scripts/sync_overleaf.py --push       # thesis/ (as committed) -> Overleaf
    python scripts/sync_overleaf.py --push --overwrite
    python scripts/sync_overleaf.py --pull       # Overleaf -> thesis/ working tree
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PREFIX = "thesis"
REMOTE = "overleaf"
BRANCH = "master"

# Output of the macro generator. Editing it on Overleaf is always a mistake --
# it is overwritten on the next regeneration, and a hand-edit pulled back into
# the repo makes the macro disagree with the results table it claims to quote.
GENERATED_DIR = "generated/"


def git(*args: str, binary: bool = False):
    """Run a git command in the repo, raising with git's own message on failure."""
    proc = subprocess.run(["git", "-C", str(REPO_ROOT), *args],
                          capture_output=True)
    if proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed:\n"
                         f"{proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout if binary else proc.stdout.decode("utf-8", "replace")


def git_ok(*args: str) -> str | None:
    """As git(), but returns None instead of exiting when the command fails.

    Needed for `rev-parse <commit>:thesis` while walking history: a commit from
    before the directory existed is a legitimate miss, not an error.
    """
    proc = subprocess.run(["git", "-C", str(REPO_ROOT), *args],
                          capture_output=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace")


def find_remote_tree_in_history(remote_head: str) -> str | None:
    """The commit whose `thesis/` tree the remote is showing, or None.

    None means the remote tree came from somewhere other than this repository
    -- in practice, an edit made in the Overleaf editor. That is the only case
    where a push destroys work, and the only case that should refuse.

    Only commits that touched PREFIX are walked, so this stays cheap and does
    not depend on total history length.
    """
    remote_tree = git("rev-parse", f"{remote_head}^{{tree}}").strip()
    revs = git("rev-list", "HEAD", "--", PREFIX).split()
    for commit in revs:
        out = git_ok("rev-parse", f"{commit}:{PREFIX}")
        if out is not None and out.strip() == remote_tree:
            return commit
    return None


def describe(commit: str) -> str:
    return (git_ok("log", "--oneline", "-1", commit) or commit).strip()


def blocking_paths(diff: dict[str, list[str]], known: str | None) -> list[str]:
    """Remote files a push would destroy that we cannot account for.

    Empty when the remote tree is recognised: everything there came from this
    repository, so a differing file is the update rather than something to
    protect. Split out from do_push so the decision can be tested without a
    network round trip -- it is the one line in this script whose being wrong
    loses writing.
    """
    return [] if known else diff["only_remote"] + diff["differing"]


def tree_files(treeish: str) -> dict[str, str]:
    """{path: blob_sha} for every file under a tree-ish, recursively."""
    out = git("ls-tree", "-r", treeish)
    files = {}
    for line in out.splitlines():
        if not line.strip():
            continue
        meta, path = line.split("\t", 1)
        _mode, obj_type, sha = meta.split()
        if obj_type == "blob":
            files[path] = sha
    return files


def uncommitted_under_prefix() -> list[str]:
    out = git("status", "--porcelain", "--", PREFIX)
    return [ln for ln in out.splitlines() if ln.strip()]


def compare(local: dict[str, str], remote: dict[str, str]) -> dict[str, list[str]]:
    return {
        # On Overleaf and not here -- someone wrote there. Blocks a push.
        "only_remote": sorted(set(remote) - set(local)),
        # Here and not on Overleaf -- new local work. Fine to push.
        "only_local": sorted(set(local) - set(remote)),
        # Both sides have it, contents differ. Blocks a push.
        "differing": sorted(p for p in set(local) & set(remote) if local[p] != remote[p]),
    }


def print_status(local: dict[str, str], remote: dict[str, str],
                 diff: dict[str, list[str]], dirty: list[str],
                 known: str | None) -> None:
    print(f"local  {PREFIX}/ (as committed at HEAD): {len(local)} files")
    print(f"remote {REMOTE}/{BRANCH}:                {len(remote)} files")
    if known:
        print(f"\n  remote tree == {PREFIX}/ at {describe(known)}")
        print("  -> nothing on Overleaf originated there; a push is a plain "
              "forward update.")
    else:
        print("\n  *** remote tree matches NO commit in this repository.")
        print("  *** Someone edited in the Overleaf editor. Pull before you "
              "push, or that writing is lost.")
    if dirty:
        print(f"\n  {len(dirty)} uncommitted change(s) under {PREFIX}/ "
              "-- a push uses the COMMITTED tree, so these would not be sent:")
        for ln in dirty[:20]:
            print(f"    {ln}")
    for key, label in [
        ("only_remote", "on Overleaf but NOT in local thesis/  (a push would DESTROY these)"),
        ("differing", "differing content between Overleaf and local thesis/"),
        ("only_local", "in local thesis/ but not yet on Overleaf  (a push would add these)"),
    ]:
        if diff[key]:
            print(f"\n  {label}: {len(diff[key])}")
            for p in diff[key][:40]:
                print(f"    {p}")
    if not any(diff.values()) and not dirty:
        print("\n  in sync -- nothing to push or pull")


def do_push(local_tree_sha: str, local: dict[str, str], remote: dict[str, str],
            diff: dict[str, list[str]], remote_head: str, overwrite: bool,
            known: str | None) -> int:
    # PROVENANCE, not content, is what decides this. A recognised remote tree
    # is an older state of our own work, so differing files are the update
    # itself rather than something to protect.
    blocking = blocking_paths(diff, known)

    if blocking and not overwrite:
        print("REFUSING TO PUSH.\n")
        print("The Overleaf tree matches no commit in this repository, so it holds content")
        print("that did not come from here -- an edit made in the Overleaf editor. Pushing")
        print("would replace the whole remote tree and that writing would be gone, with no")
        print("conflict and no warning: the push is a legitimate fast-forward.\n")
        if diff["only_remote"]:
            print(f"  files only on Overleaf ({len(diff['only_remote'])}):")
            for p in diff["only_remote"]:
                print(f"    {p}")
        if diff["differing"]:
            print(f"  files whose content differs ({len(diff['differing'])}):")
            for p in diff["differing"]:
                print(f"    {p}")
        print("\nBring them down first:  python scripts/sync_overleaf.py --pull")
        print("Or, only if you are certain the Overleaf side should be discarded:")
        print("                        python scripts/sync_overleaf.py --push --overwrite")
        return 1

    if known:
        print(f"remote tree == {PREFIX}/ at {describe(known)} -- forward update, "
              "no Overleaf-side content at risk.")
        # Reported even though it is not blocking: on a recognised remote this
        # means a deliberate local deletion, and it still removes the file from
        # a live Overleaf project.
        if diff["only_remote"]:
            print(f"  NOTE -- {len(diff['only_remote'])} file(s) will be DELETED from "
                  "Overleaf, having been removed locally:")
            for p in diff["only_remote"]:
                print(f"    {p}")

    if overwrite and blocking:
        print(f"--overwrite: discarding {len(blocking)} file(s) of Overleaf-side content.\n")

    remote_tree = git("rev-parse", f"{remote_head}^{{tree}}").strip()
    if remote_tree == local_tree_sha:
        print("Overleaf already matches the committed thesis/ tree -- nothing to push.")
        return 0

    head = git("rev-parse", "--short", "HEAD").strip()
    message = (
        f"Sync thesis/ from experiment repo @ {head}\n\n"
        "Pushed by scripts/sync_overleaf.py. Files under generated/ are produced by\n"
        "scripts/build_thesis_macros.py from the results tables -- do not edit them\n"
        "here; they are overwritten on the next regeneration."
    )
    # Parented on the CURRENT remote head, so this is a fast-forward and no
    # force is ever needed -- which matters, because Overleaf refuses force.
    new_commit = git("commit-tree", local_tree_sha, "-p", remote_head,
                     "-m", message).strip()
    print(f"pushing {new_commit[:12]} (parent {remote_head[:12]}) -> {REMOTE}/{BRANCH}")
    print(git("push", REMOTE, f"{new_commit}:{BRANCH}"))
    print("pushed. Recompile on Overleaf to pick up the change.")
    return 0


def do_pull(remote: dict[str, str], diff: dict[str, list[str]]) -> int:
    """Write Overleaf's blobs into thesis/. No staging, no commit."""
    changed, added = [], []
    for path, sha in sorted(remote.items()):
        dest = REPO_ROOT / PREFIX / path
        blob = git("cat-file", "blob", sha, binary=True)
        if dest.exists():
            if dest.read_bytes() == blob:
                continue
            changed.append(path)
        else:
            added.append(path)
            dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(blob)

    for label, items in [("added", added), ("modified", changed)]:
        if items:
            print(f"{label}: {len(items)}")
            for p in items:
                print(f"  {p}")
    if not added and not changed:
        print("thesis/ already matches Overleaf -- nothing written.")

    # Deliberately NOT deleted: removing a local file because Overleaf lacks it
    # is exactly the destructive-by-omission move this script exists to avoid.
    if diff["only_local"]:
        print(f"\nNOT deleted -- present locally, absent on Overleaf "
              f"({len(diff['only_local'])}):")
        for p in diff["only_local"]:
            print(f"  {p}")
        print("  Delete them yourself if Overleaf is right; they are left alone here.")

    touched = [p for p in added + changed if p.startswith(GENERATED_DIR)]
    if touched:
        print(f"\n*** WARNING: {len(touched)} file(s) under {GENERATED_DIR} changed on "
              "Overleaf.")
        print("*** That directory is GENERATED. A hand-edit there makes a macro disagree")
        print("*** with the results table it quotes. Discard these and re-run")
        print("*** scripts/build_thesis_macros.py unless you know otherwise:")
        for p in touched:
            print(f"      {p}")

    if added or changed:
        print(f"\nNothing was committed. Review with:  git diff -- {PREFIX}/")
    return 0


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    action = ap.add_mutually_exclusive_group()
    action.add_argument("--push", action="store_true",
                        help=f"send the COMMITTED {PREFIX}/ tree to Overleaf")
    action.add_argument("--pull", action="store_true",
                        help=f"write Overleaf's files into {PREFIX}/ (no commit)")
    ap.add_argument("--overwrite", action="store_true",
                    help="allow --push to discard Overleaf-side content. Deliberate only.")
    args = ap.parse_args()

    if args.overwrite and not args.push:
        return ap.error("--overwrite is only meaningful with --push")

    remotes = git("remote").split()
    if REMOTE not in remotes:
        raise SystemExit(f"no git remote named {REMOTE!r}. Add it with:\n"
                         f"  git remote add {REMOTE} <overleaf git url>")

    git("fetch", REMOTE)  # read-only
    remote_head = git("rev-parse", f"{REMOTE}/{BRANCH}").strip()
    local_tree_sha = git("rev-parse", f"HEAD:{PREFIX}").strip()

    local = tree_files(f"HEAD:{PREFIX}")
    remote = tree_files(f"{REMOTE}/{BRANCH}")
    diff = compare(local, remote)
    dirty = uncommitted_under_prefix()
    known = find_remote_tree_in_history(remote_head)

    if not args.push and not args.pull:
        print_status(local, remote, diff, dirty, known)
        print("\nNo action taken. Pass --push or --pull.")
        return 0

    if args.push:
        if dirty:
            print(f"REFUSING TO PUSH: {len(dirty)} uncommitted change(s) under {PREFIX}/.")
            print("A push sends the COMMITTED tree, so these would be silently omitted "
                  "and Overleaf would disagree with your working copy.")
            for ln in dirty:
                print(f"  {ln}")
            print("\nCommit them first, then push.")
            return 1
        return do_push(local_tree_sha, local, remote, diff, remote_head,
                       args.overwrite, known)

    return do_pull(remote, diff)


if __name__ == "__main__":
    sys.exit(main())
