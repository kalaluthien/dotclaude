#!/usr/bin/env python3
"""Claude Code hook (PreToolUse on every tool, UserPromptSubmit): refuse a session that works in a protected folder, and
a tool call that names a path inside one, by any spelling, or scans a folder above one.

A protected folder is `~/Downloads` and each `Read(~/<dir>/**)` or `Read(//<dir>/**)` deny rule of the user settings, so one deny rule
protects a folder in both layers: Claude Code's own permission check and this hook, which catches the forms that check
misses (`$HOME`, `cd`, relative paths, `..`, globs, inline code, recursive scans).

usage: refuse-downloads.py < hook-input.json
       refuse-downloads.py start [<claude argument>...]
         exits 2 when the current folder, or an argument naming an existing folder (`--add-dir <dir>`), lies in a
         protected folder; `scripts/protect-folders.zsh` runs it before Claude Code starts, since a session started
         there loads that folder's project skills, agents, hooks and MCP servers before any hook can refuse
"""
import fnmatch
import json
import os
import re
import shlex
import sys

HOME = os.path.expanduser("~")
SETTINGS = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(HOME, ".claude"), "settings.json")
ALWAYS = ["~/Downloads", "~/Documents"]  # protected even with no deny rule
RULE = re.compile(r"^Read\((~/|//)(.+?)/\*\*\)$")
VARIABLES = [
    (re.compile(r"\$\{HOME(?::?[-=+?][^}]*)?\}|\$HOME\b"), HOME),
    (re.compile(r"\$\{USER\}|\$USER\b"), os.path.basename(HOME)),
    (re.compile(r"(?<![\w/.~-])~(?=/|$|[\s'\"`:;,)\]}])"), HOME),
]
HOME_HINT = re.compile(r"~|\bHOME\b|home\(|homedir|expanduser|Path\.home")
SPLIT = re.compile(r"[\s'\"`(){},;|&<>=:]+")
ASSIGNMENT = re.compile(r"(?:^|[\s;&|(])([A-Za-z_]\w*)=([^\s;&|)]*)")
BARE_CD = re.compile(r"(?:^|[\s;&|(])cd\s*(?=$|[;&|)])")
GLOB = re.compile(r"[*?\[]")
BRACE = re.compile(r"(?<!\$)\{([^{}]*)\}")
SEPARATORS = re.compile(r"\|\||&&|[;|&\n]|\$\(|`")
WRAPPERS = {"sudo", "env", "nice", "nohup", "time", "exec", "command", "xargs", "timeout", "caffeinate"}
ALWAYS_RECURSIVE = {"find", "fd", "rg", "ag", "du", "tree", "mdfind", "rsync", "zip", "tar", "ditto"}
RECURSIVE_WORDS = {"--recursive", "--dereference-recursive", "--directories=recurse", "-drecurse", "recurse"}
RECURSIVE_FLAG = {"grep": "rR", "egrep": "rR", "fgrep": "rR", "ls": "R", "cp": "rRa", "chmod": "R", "chown": "R",
                  "chflags": "R", "xattr": "r", "rm": "rR", "scp": "r"}
PATH_KEYS = {"file_path", "notebook_path", "path"}


def folders():
    """The protected folders, absolute, from the Read deny rules of the user settings."""
    try:
        with open(SETTINGS) as handle:
            deny = (json.load(handle).get("permissions") or {}).get("deny") or []
    except (OSError, ValueError):
        deny = []
    found = [os.path.expanduser(f) for f in ALWAYS]
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


def braces(word, limit=64):
    """WORD with each `{a,b}` group expanded, as the shell does, up to LIMIT words."""
    match = BRACE.search(word)
    if not match:
        return [word]
    found = []
    for option in match.group(1).split(","):
        found += braces(word[:match.start()] + option + word[match.end():], limit)
        if len(found) >= limit:
            break
    return found[:limit]


def unbrace(text):
    return " ".join(" ".join(braces(word)) for word in text.split(" "))


def check_word(word, bases, protected):
    """The protected folder WORD names, read as a path from each base, else None."""
    if not word or word.startswith("-") and "/" not in word:
        return None
    if word.startswith("/"):
        candidates = [word] + ([os.path.join(HOME, word.lstrip("/"))] if HOME in bases else [])
    else:
        candidates = [os.path.join(base, word) for base in bases]
    for candidate in candidates:
        hit = glob_reaches(candidate, protected) if GLOB.search(candidate) else inside(candidate, protected)
        if hit:
            return hit
    return None


def scans(command, bases, protected):
    """The protected folder a recursive command in COMMAND reaches by scanning a folder above it, read from each base
    folder the command starts in or moves to, else None."""
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
        letters = RECURSIVE_FLAG.get(program, "")
        recursive = program in ALWAYS_RECURSIVE or bool(letters) and any(
            w in RECURSIVE_WORDS or re.match(r"^-[A-Za-z]*[" + letters + "]", w) for w in rest)
        if not recursive:
            continue
        for base in bases:
            targets = [w for w in rest if not w.startswith("-") and (w.startswith("/") or os.path.exists(os.path.join(base, w)))]
            if program == "mdfind" and "-onlyin" not in rest:
                targets = ["/"]
            for target in targets or [base]:
                hit = above(os.path.join(base, target), protected)
                if hit:
                    return hit
    return None


def variants(command):
    """COMMAND as written, then with quotes and backslashes dropped and simple `name=value` variables put in, so a
    path split by quotes or built from variables reads whole."""
    joined = re.sub(r"\$([A-Za-z_]\w*)(?=['\"])", r"${\1}", command)
    joined = re.sub(r"[\\'\"]", "", joined)
    values = {name: value for name, value in ASSIGNMENT.findall(joined)}
    for _ in range(3):
        for name, value in values.items():
            joined = re.sub(r"\$\{" + name + r"\}|\$" + name + r"\b", lambda _: value, joined)
    texts = [re.sub(r"file://localhost(?=/)", "file://", t) for t in (command, joined)]
    return [expand(t) for t in texts] + [expand(unbrace(t)) for t in texts]


def check_command(command, cwd, protected):
    for text in variants(command):
        hit = check_text(text, command, cwd, protected)
        if hit:
            return hit
    return None


def check_text(text, command, cwd, protected):
    moves = [cwd] + ([HOME] if BARE_CD.search(text) else [])
    for match in re.finditer(r"(?:^|[\s;&|(])(?:cd|pushd)\s+(?:-[LPe@]+\s+)*([^\s;&|)]+)", text):
        try:
            target = shlex.split(match.group(1))[0]
        except (ValueError, IndexError):
            target = match.group(1)
        moves.append(os.path.join(cwd, target))
    bases = moves + ([HOME] if HOME_HINT.search(command) else [])
    for word in SPLIT.split(text):
        hit = check_word(word, bases, protected)
        if hit:
            return hit
    return scans(text, moves, protected)


def check_tool(name, tool_input, cwd, protected):
    if not isinstance(tool_input, dict):
        return None
    if isinstance(tool_input.get("command"), str):
        return check_command(tool_input["command"], cwd, protected)
    if name == "Glob":
        base = os.path.join(cwd, expand(tool_input.get("path") or "."))
        for pattern in braces(expand(tool_input.get("pattern") or "")):
            pattern = os.path.join(base, pattern)
            hit = glob_reaches(pattern, protected) or ("**" in pattern and above(base, protected))
            if hit:
                return hit
        return inside(base, protected)
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
                hit = "/" in word and check_word(word, [cwd], protected)
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


def start(args):
    protected = folders()
    cwd = os.getcwd()
    named = [part for arg in args for part in arg.split("=", 1)[-1:]]
    for path in [cwd] + [os.path.join(cwd, os.path.expanduser(a)) for a in named if a and not a.startswith("-")]:
        hit = (path == cwd or os.path.isdir(path)) and inside(path, protected)
        if hit:
            print(f"refuse-downloads: Claude Code does not start with {hit}, a protected folder, as its folder or an "
                  f"added one: start it elsewhere. A protected folder is ~/Downloads or a Read deny rule in {SETTINGS}.", file=sys.stderr)
            return 2
    return 0


def main():
    if sys.argv[1:2] == ["start"]:
        return start(sys.argv[2:])
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
    print(f"refuse-downloads: {reason}. A protected folder is ~/Downloads or a Read deny rule in {SETTINGS}; "
          "Claude never reads, lists, changes or works in it.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
