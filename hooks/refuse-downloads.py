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
HOME_HINT = re.compile(r"\bHOME\b|home\(|homedir|expanduser|Path\.home")
SPLIT = re.compile(r"[\s'\"`(){},;|&<>=:]+")
ASSIGNMENT = re.compile(r"(?:^|[\s;&|(])([A-Za-z_]\w*)=([^\s;&|)]*)")
BARE_CD = re.compile(r"(?:^|[\s;&|(])cd\s*(?=$|[;&|)])")
GLOB = re.compile(r"[*?\[]")
BRACE = re.compile(r"(?<!\$)\{([^{}]*)\}")
HEREDOC = re.compile(r"<<(-?)[ \t]*(\\?)([\"']?)([\w.-]+)\3")
SHELLS = {"sh", "bash", "zsh", "dash", "ksh"}
SUBSTITUTED = "\x01"
ANSI_QUOTED = re.compile(r"\$'((?:\\.|[^'\\])*)'")
SHELL_INPUT = SHELLS | {"eval", "source", "."}
WRAPPERS = {"sudo", "env", "nice", "nohup", "time", "exec", "command", "xargs", "timeout", "caffeinate"}
ALWAYS_RECURSIVE = {"find", "fd", "rg", "ag", "du", "tree", "mdfind", "rsync", "zip", "tar", "ditto"}
RECURSIVE_WORDS = {"--recursive", "--dereference-recursive", "--directories=recurse", "-drecurse", "recurse"}
RECURSIVE_FLAG = {"grep": "rR", "egrep": "rR", "fgrep": "rR", "ls": "R", "cp": "rRa", "chmod": "R", "chown": "R",
                  "chflags": "R", "xattr": "r", "rm": "rR", "scp": "r"}
SAFE_COPY = re.compile(r"^\s*cp(?: +[\w@%+,./~-]+)+\s*$")
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
    """The protected folder WORD names, read as a path from each base, else None. A bare `~` sets no home base, since
    `expand` already made it an absolute path, so only code that builds a home path sets one."""
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


class Body(str):
    """A line of a heredoc body, which is data unless a shell reads it."""


def heredoc_body(text, i, delimiter, tabbed, literal):
    """The commands of the heredoc body that starts at I, up to its DELIMITER line, read as the shell reads a body (quotes
    are plain text, a substitution still runs unless LITERAL), and the index after it."""
    lines = []
    while i < len(text):
        end = text.find("\n", i)
        end = len(text) if end < 0 else end
        line, i = text[i:end], end + 1
        if (line.lstrip("\t") if tabbed else line) == delimiter:
            break
        lines.append(line)
    return parse("\n".join(lines), literal=literal, data=True, plain=True)[0], i


def parse(text, i=0, end="", literal=False, data=False, plain=False):
    """The simple commands of TEXT read from I as the shell reads them, up to the unquoted END character (the `)` of a
    `$(...)`, a closing backtick), and the index after it. A `;`, `|`, `&` or newline splits only outside quotes; a
    substitution is read as a command of its own and leaves one word in its outer command; a heredoc body is read line
    by line, and holds no substitution when LITERAL, its delimiter being quoted; DATA marks the commands outside a
    substitution as `Body`; PLAIN reads a heredoc body, where a quote, a `#` and a heredoc are plain text."""
    found, current, quote, heredocs = [], "", None, []
    kind = Body if data else str
    while i < len(text):
        c, heredoc = text[i], HEREDOC.match(text, i) if text.startswith("<<", i) else None
        step = 1
        if quote == "'":
            quote = None if c == "'" else quote
        elif c == "\\":
            step = 2
        elif c == end and quote is None:
            i += 1
            break
        elif not literal and c == "`":
            stop = i + 1
            while stop < len(text) and text[stop] != "`":
                stop += 2 if text[stop] == "\\" else 1
            inner = parse(re.sub(r"\\([`\\])", r"\1", text[i + 1:stop]))[0]
            i = stop + 1
            found += [kind(current)] + inner if quote is None else inner
            current = "" if quote is None else current + SUBSTITUTED
            continue
        elif not literal and text.startswith("$(", i):
            inner, i = parse(text, i + 2, ")")
            found += [kind(current)] + inner if quote is None else inner
            current = "" if quote is None else current + SUBSTITUTED
            continue
        elif quote is None and not plain and c == "#" and not current[-1:].strip():
            i = text.find("\n", i) if "\n" in text[i:] else len(text)
            continue
        elif quote is None and not plain and text.startswith("$'", i):
            j = i + 2
            while j < len(text) and text[j] != "'":
                j += 2 if text[j] == "\\" else 1
            current += text[i:j + 1]
            i = j + 1
            continue
        elif not plain and c in "'\"" and quote in (None, c):
            quote = None if quote else c
        elif quote is None and not plain and heredoc and text[i - 1:i] != "<":
            heredocs.append((heredoc.group(4), bool(heredoc.group(1)), bool(heredoc.group(2) or heredoc.group(3))))
            current += heredoc.group(0)
            i = heredoc.end()
            continue
        elif quote is None and c in ";|&\n":
            found.append(kind(current))
            current, i = "", i + 1
            while c == "\n" and heredocs:
                delimiter, tabbed, quoted = heredocs.pop(0)
                body, i = heredoc_body(text, i, delimiter, tabbed, quoted)
                found += body
            continue
        current += text[i:i + step]
        i += step
    return found + [kind(current)], i


def ansi(match):
    """The ANSI-C quoted word `$'...'` as a plain quoted word."""
    try:
        return shlex.quote(match.group(1).encode("latin-1", "backslashreplace").decode("unicode_escape"))
    except (UnicodeError, ValueError):
        return shlex.quote(match.group(1))


def scans(command, bases, protected):
    """The protected folder a recursive command in COMMAND reaches by scanning a folder above it, read from each base
    folder the command starts in or moves to, else None."""
    chunks = parse(command)[0]
    shell = any(os.path.basename(w) in SHELL_INPUT and (os.path.basename(w) != "." or i < len(words) - 1)  # `source` needs a file
                for words in (re.findall(r"[^\s<>|&;()]+", c) for c in chunks if not isinstance(c, Body))
                for i, w in enumerate(words))
    commands = []
    for chunk in chunks:
        if not isinstance(chunk, Body):
            commands.append(chunk)
        elif shell:
            commands += parse(chunk)[0]
    for chunk in commands:
        try:
            words = shlex.split(ANSI_QUOTED.sub(ansi, chunk))
        except ValueError:
            words = chunk.split()
        while words and (re.match(r"^[A-Za-z_]\w*=", words[0]) or os.path.basename(words[0]) in WRAPPERS):
            words = words[1:]
        if not words:
            continue
        program, rest = os.path.basename(words[0]), words[1:]
        code = next((rest[i + 1] for i, w in enumerate(rest[:-1]) if re.match(r"^-\w*c\w*$", w)), None) \
            if program in SHELLS else " ".join(rest) if program == "eval" else None
        here = []
        for k, w in enumerate(rest if program in SHELLS else []):
            if w == "<<<" and k + 1 < len(rest):
                here.append(rest[k + 1])
            elif w.startswith("<<<") and len(w) > 3:
                here.append(w[3:])
        for code in [c for c in [code] + here if c]:
            hit = scans(re.sub(r"\\([$`\"\\])", r"\1", code), bases, protected)
            if hit:
                return hit
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
    path split by quotes or built from variables reads whole; each text pairs with the same text keeping its quotes,
    which `parse` needs to tell a separator from a quoted character."""
    spaced = re.sub(r"\$([A-Za-z_]\w*)(?=['\"])", r"${\1}", command)
    joined = re.sub(r"[\\'\"]", "", spaced)
    values = {name: value for name, value in ASSIGNMENT.findall(joined)}

    def fill(text):
        for _ in range(3):
            for name, value in values.items():
                text = re.sub(r"\$\{" + name + r"\}|\$" + name + r"\b", lambda _: value, text)
        return text

    pairs = [(command, command), (fill(joined), fill(spaced))]
    pairs = [tuple(re.sub(r"file://localhost(?=/)", "file://", t) for t in pair) for pair in pairs]
    return [tuple(expand(t) for t in pair) for pair in pairs] + [tuple(expand(unbrace(t)) for t in pair) for pair in pairs]


def copies_file_out(command, cwd, protected):
    """True when COMMAND is one plain `cp` (flags `-p`, `-X` only) of named regular files, all inside a protected folder,
    to a destination outside every protected folder: copying a file out reads nothing else of the folder."""
    if not SAFE_COPY.match(command):
        return False
    try:
        words = shlex.split(command)
    except ValueError:
        return False
    words = words[1:]
    while words and re.match(r"^-[pX]+$", words[0]):
        words = words[1:]
    if len(words) < 2:
        return False
    paths = []
    for word in words:
        if word.startswith("-") or (word.startswith("~") and not word.startswith("~/")):
            return False
        paths.append(os.path.join(cwd, os.path.expanduser(word)))
    *sources, destination = paths
    if os.path.isdir(destination):
        written = [os.path.join(destination, os.path.basename(source)) for source in sources]
    elif len(sources) == 1 and (os.path.isfile(destination) or not os.path.lexists(destination)
                                and os.path.isdir(os.path.dirname(destination))):
        written = [destination]
    else:
        return False  # a device such as /dev/stdout would print the file into the session
    if any(os.path.lexists(path) and (os.path.islink(path) or not os.path.isfile(path)) for path in written):
        return False  # an existing link or device at the target could print the file into the session
    return not any(inside(path, protected) for path in written) and all(
        inside(source, protected) and os.path.isfile(source) and not os.path.islink(source) for source in sources)


def check_command(command, cwd, protected):
    if copies_file_out(command, cwd, protected):
        return None
    for text, kept in variants(command):
        hit = check_text(text, kept, command, cwd, protected)
        if hit:
            return hit
    return None


def check_text(text, kept, command, cwd, protected):
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
    return scans(kept, moves, protected)


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
