#!/usr/bin/env python3
"""Claude Code hook (PreToolUse on every tool, UserPromptSubmit): refuse a session that works in a protected folder, and
a tool call that names a path inside one, by any spelling, or scans a folder above one.

A protected folder is each `Read(~/<dir>/**)` or `Read(//<dir>/**)` deny rule of the user settings, so one deny rule
protects a folder in both layers: Claude Code's own permission check and this hook, which catches the forms that check
misses (`$HOME`, `cd`, relative paths, `..`, globs, inline code, recursive scans).

usage: protect-folders.py < hook-input.json
"""
import fnmatch
import json
import os
import re
import shlex
import sys

HOME = os.path.expanduser("~")
SETTINGS = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(HOME, ".claude"), "settings.json")
FALLBACK = ["~/Downloads"]  # when the settings cannot be read
RULE = re.compile(r"^Read\((~/|//)(.+?)/\*\*\)$")
VARIABLES = [
    (re.compile(r"\$\{HOME\}|\$HOME\b"), HOME),
    (re.compile(r"\$\{USER\}|\$USER\b"), os.path.basename(HOME)),
    (re.compile(r"(?<![\w/.~-])~(?=/|$|[\s'\"`:;,)\]}])"), HOME),
]
HOME_HINT = re.compile(r"~|\bHOME\b|home\(|homedir|expanduser|Path\.home")
SPLIT = re.compile(r"[\s'\"`()\[\]{},;|&<>=:]+")
GLOB = re.compile(r"[*?\[]")
SEPARATORS = re.compile(r"\|\||&&|[;|&\n]|\$\(|`")
WRAPPERS = {"sudo", "env", "nice", "nohup", "time", "exec", "command", "xargs", "timeout", "caffeinate"}
ALWAYS_RECURSIVE = {"find", "fd", "rg", "ag", "du", "tree", "mdfind", "rsync", "zip", "tar", "ditto"}
RECURSIVE_FLAG = {"grep": "rR", "egrep": "rR", "fgrep": "rR", "ls": "R", "cp": "rRa", "chmod": "R", "chown": "R",
                  "chflags": "R", "xattr": "r", "rm": "rR", "scp": "r"}
PATH_KEYS = {"file_path", "notebook_path", "path"}


def folders():
    """The protected folders, absolute, from the Read deny rules of the user settings."""
    try:
        with open(SETTINGS) as handle:
            deny = (json.load(handle).get("permissions") or {}).get("deny") or []
    except (OSError, ValueError):
        return [os.path.expanduser(f) for f in FALLBACK]
    found = []
    for rule in deny:
        match = RULE.match(rule) if isinstance(rule, str) else None
        if match:
            found.append(os.path.join(HOME, match.group(2)) if match.group(1) == "~/" else "/" + match.group(2))
    return found


def fold(path):
    return path.casefold() if sys.platform == "darwin" else path


def spellings(path):
    """The normalized path and the path with every symlink resolved, so `..` and a link into a folder both count."""
    return {fold(os.path.normpath(path)), fold(os.path.realpath(path))}


def inside(path, protected):
    """The protected folder PATH lies in or equals, else None."""
    for folder in protected:
        for f in spellings(folder):
            if any(p == f or p.startswith(f.rstrip("/") + "/") for p in spellings(path)):
                return folder
    return None


def above(path, protected):
    """The protected folder that lies strictly below PATH, so a recursive scan of PATH reaches it, else None."""
    for folder in protected:
        for f in spellings(folder):
            if any(f.startswith(p.rstrip("/") + "/") for p in spellings(path)):
                return folder
    return None


def glob_reaches(pattern, protected):
    """The protected folder an absolute glob PATTERN can name or descend into, else None."""
    parts = [p for p in fold(os.path.normpath(pattern)).split("/") if p]
    for folder in protected:
        for f in spellings(folder):
            target = [p for p in f.split("/") if p]
            for i, part in enumerate(parts):
                if part == "**":
                    return folder
                if i >= len(target) or not fnmatch.fnmatchcase(target[i], part):
                    break
                if i == len(target) - 1:
                    return folder
    return None


def expand(text):
    for pattern, value in VARIABLES:
        text = pattern.sub(lambda _: value, text)
    return text


def check_word(word, bases, protected):
    """The protected folder WORD names, read as a path from each base, else None."""
    if not word or word.startswith("-") and "/" not in word:
        return None
    candidates = [word] if word.startswith("/") else [os.path.join(base, word) for base in bases]
    for candidate in candidates:
        hit = glob_reaches(candidate, protected) if GLOB.search(candidate) else inside(candidate, protected)
        if hit:
            return hit
    return None


def scans(command, cwd, protected):
    """The protected folder a recursive command in COMMAND reaches by scanning a folder above it, else None."""
    for chunk in SEPARATORS.split(command):
        try:
            words = shlex.split(chunk)
        except ValueError:
            words = chunk.split()
        while words and (re.match(r"^[A-Za-z_]\w*=", words[0]) or os.path.basename(words[0]) in WRAPPERS):
            words = words[1:]
        if not words:
            continue
        program, rest = os.path.basename(words[0]), words[1:]
        flags = [w for w in rest if w.startswith("-")]
        letters = RECURSIVE_FLAG.get(program, "")
        recursive = program in ALWAYS_RECURSIVE or bool(letters) and any(
            w == "--recursive" or re.match(r"^-[A-Za-z]*[" + letters + "]", w) for w in flags)
        if not recursive:
            continue
        targets = [w for w in rest if not w.startswith("-") and (w.startswith("/") or os.path.exists(os.path.join(cwd, w)))]
        if program == "mdfind" and "-onlyin" not in rest:
            targets = ["/"]
        for target in targets or [cwd]:
            hit = above(os.path.join(cwd, target), protected)
            if hit:
                return hit
    return None


def check_command(command, cwd, protected):
    text = expand(command)
    bases = [cwd]
    for match in re.finditer(r"(?:^|[\s;&|(])(?:cd|pushd)\s+(?:-[LPe@]+\s+)*([^\s;&|)]+)", text):
        try:
            target = shlex.split(match.group(1))[0]
        except (ValueError, IndexError):
            target = match.group(1)
        bases.append(os.path.join(cwd, target))
    if HOME_HINT.search(command):
        bases.append(HOME)
    for word in SPLIT.split(text):
        hit = check_word(word, bases, protected)
        if hit:
            return hit
    return scans(text, cwd, protected)


def check_tool(name, tool_input, cwd, protected):
    if not isinstance(tool_input, dict):
        return None
    if isinstance(tool_input.get("command"), str):
        return check_command(tool_input["command"], cwd, protected)
    if name == "Glob":
        base = os.path.join(cwd, expand(tool_input.get("path") or "."))
        pattern = os.path.join(base, expand(tool_input.get("pattern") or ""))
        return inside(base, protected) or glob_reaches(pattern, protected) or (
            "**" in pattern and above(base, protected))
    if name == "Grep":
        base = os.path.join(cwd, expand(tool_input.get("path") or "."))
        return inside(base, protected) or above(base, protected)
    for key, value in tool_input.items():
        if key in PATH_KEYS and isinstance(value, str):
            hit = check_word(expand(value), [cwd], protected)
            if hit:
                return hit
    if name.startswith("mcp__"):
        for value in strings(tool_input):
            for word in SPLIT.split(expand(value)):
                hit = word.startswith("/") and check_word(word, [], protected)
                if hit:
                    return hit
    return None


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def main():
    event = json.load(sys.stdin)
    protected = folders()
    cwd = event.get("cwd") or os.getcwd()
    hit = inside(cwd, protected)
    if hit:
        reason = f"this session works in {hit}, a protected folder: start Claude in another folder"
    else:
        hit = check_tool(event.get("tool_name") or "", event.get("tool_input"), cwd, protected)
        reason = f"this call reaches {hit}, a protected folder: name a path outside it, and scan no folder above it"
    if not hit:
        return 0
    print(f"protect-folders: {reason}. A protected folder is a Read deny rule in {SETTINGS}; "
          "Claude never reads, lists, changes or works in it.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
