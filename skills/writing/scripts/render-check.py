#!/usr/bin/env python3
"""Render one view and report what the render shows.

    render-check.py <view.html> [--out DIR]

Prints the two PNG paths, the layout width each render got, and three
verdicts: the page opening, the SVG markup, and the figure geometry. Exits 0
when every check passes, 1 when one fails, and 2 when the machine cannot run
the check at all. Without --out the images land in a temporary directory,
whose path is printed.

The page verdict covers what an image cannot show: the doctype, the lang, the
charset, the viewport meta, an <h1> ahead of everything else in the body, and
a provenance block carrying Doctype, Question or Goal, and Updated, and never
Reviewed.

Three facts the caller cannot observe:

  * Headless Chrome on macOS does not lay out below 500 CSS units. A smaller
    --window-size still lays the page out at 500 and crops the image, which
    reads as text cut off at the right edge that the browser never drew. This
    script measures the width it actually got, with window.innerWidth on a
    probe page, and prints it beside each render.
  * A screenshot captures exactly the window height, so a fixed height crops a
    longer page silently. This script captures far past any view and then
    trims the blank tail, so the image is the whole page.
  * A screenshot also cannot show sideways overflow: content past the right
    edge is cropped away and the image looks clean. This script compares the
    document's scrollWidth against the viewport at each width instead.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

WIDE = 1120
NARROW = 500
CAPTURE_HEIGHT = 16000
TAIL_MARGIN = 24

CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "chromium",
)
# The guard is this script's sibling in the skill, so a checkout runs the
# guard it ships with rather than whichever copy happens to be installed.
FIGURE_HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check-figures")

FIGURE = re.compile(r"<figure\b.*?</figure>", re.S)
SVG = re.compile(r"<svg\b.*?</svg>", re.S)
SVG_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S)
ID = re.compile(r'\bid="([^"]+)"')
REF = re.compile(r"url\(#([^)]+)\)")
HOOK_FINDING = re.compile(r":\d+: ")
DT = re.compile(r"<dt[^>]*>(.*?)</dt>", re.S)
PROVENANCE = re.compile(r'<dl[^>]*class="[^"]*\bprovenance\b[^"]*".*?</dl>', re.S)


def fail(message, code=2):
    print(f"render-check.py: {message}", file=sys.stderr)
    sys.exit(code)


def find_chrome():
    for candidate in CHROME_CANDIDATES:
        if os.path.sep in candidate:
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate
        else:
            found = shutil.which(candidate)
            if found:
                return found
    return None


def run_chrome(chrome, args):
    """Chrome writes noise to stderr on every run, so only stdout is kept."""
    try:
        done = subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--hide-scrollbars", *args],
            capture_output=True,
            text=True,
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        fail("Chrome did not finish in 180 seconds")
    except OSError as error:
        fail(f"Chrome did not start: {error}")
    return done.stdout


def layout_width(chrome, scratch, requested):
    """The CSS width the page is actually laid out at, or None when unread."""
    probe = os.path.join(scratch, "probe.html")
    with open(probe, "w", encoding="utf-8") as handle:
        handle.write(
            "<!doctype html><html><body><p id=o></p><script>"
            "document.getElementById('o').textContent='IW='+window.innerWidth;"
            "</script></body></html>"
        )
    out = run_chrome(chrome, ["--dump-dom", f"--window-size={requested},800", probe])
    match = re.search(r"IW=(\d+)", out)
    return int(match.group(1)) if match else None


def sideways(chrome, scratch, source, width, label):
    """(scrollWidth, innerWidth) of the page at one width, or (None, None).

    The view carries no script of its own, so the measurement runs on a copy
    with one probe appended. A copy is used rather than the view because this
    script never edits what it checks, and one empty paragraph changes no
    horizontal layout. The page is self-contained by rule, so the copy renders
    the same wherever it sits.
    """
    probe = os.path.join(scratch, f"probe-{label}.html")
    marker = (
        '<p id="rc-probe"></p><script>document.getElementById("rc-probe")'
        '.textContent="SW="+document.documentElement.scrollWidth'
        '+" IW="+window.innerWidth;</script>'
    )
    body = source.replace("</body>", marker + "</body>", 1)
    if body == source:
        body = source + marker
    with open(probe, "w", encoding="utf-8") as handle:
        handle.write(body)
    out = run_chrome(chrome, ["--dump-dom", f"--window-size={width},900", probe])
    match = re.search(r"SW=(\d+) IW=(\d+)", out)
    return (int(match.group(1)), int(match.group(2))) if match else (None, None)


def shoot(chrome, view, png, width):
    run_chrome(
        chrome,
        [
            f"--screenshot={png}",
            f"--window-size={width},{CAPTURE_HEIGHT}",
            view,
        ],
    )
    return os.path.isfile(png)


def trim(png):
    """Cut the blank tail. Returns (width, height, whole_page)."""
    try:
        from PIL import Image
    except ImportError:
        return (None, None, None)
    with Image.open(png) as image:
        image = image.convert("RGB")
        width, height = image.size
        mask = image.convert("L").point(lambda value: 0 if value > 250 else 255)
        box = mask.getbbox()
        if box is None:
            return (width, height, True)
        bottom = min(height, box[3] + TAIL_MARGIN)
        image.crop((0, 0, width, bottom)).save(png)
        return (width, bottom, box[3] < height - 1)


def check_page(source):
    """The head and opening rules a rendered image cannot show."""
    findings = []
    split = source.find("<body")
    head, body = (source[:split], source[split:]) if split > 0 else (source, "")
    if not source.lstrip()[:15].lower().startswith("<!doctype html>"):
        findings.append("the page does not open with <!doctype html>")
    if not re.search(r"<html[^>]*\blang=", head):
        findings.append("<html> carries no lang attribute")
    if not re.search(r"<meta[^>]*charset=", head, re.I):
        findings.append("the head carries no charset meta; box drawing and Korean break")
    if not re.search(r"""<meta[^>]*name=["']viewport""", head, re.I):
        findings.append("the head carries no viewport meta; a phone lays the page out at 980 px")
    marks = [body.find(tag) for tag in ("<h1", "<h2", 'class="provenance"')]
    if marks[0] < 0:
        findings.append("the body carries no <h1>")
    elif marks[2] >= 0 and marks[0] > marks[2]:
        findings.append("the provenance block opens the page ahead of the <h1>")
    elif marks[1] >= 0 and marks[0] > marks[1]:
        findings.append("a section heading opens the page ahead of the <h1>")
    block = PROVENANCE.search(body)
    if not block:
        findings.append('no <dl class="provenance"> block; every reader parses one')
    else:
        terms = {t.strip().rstrip(":").casefold() for t in DT.findall(block.group(0))}
        for role in ("doctype", "updated"):
            if role not in terms:
                findings.append(f"the provenance block carries no {role.title()} term")
        if not terms & {"question", "goal"}:
            findings.append("the provenance block carries neither Question nor Goal")
        if "reviewed" in terms:
            findings.append("the provenance block carries Reviewed, which this skill never writes")
    return findings


def check_svg(source):
    """One finding per figure whose markup or marker set is wrong.

    Only an <svg> inside a <figure> is a figure, which is the same scope
    check-figures uses; an svg elsewhere on the page is decoration.
    """
    findings = []
    blocks = [svg for figure in FIGURE.findall(source) for svg in SVG.findall(figure)]
    for index, block in enumerate(blocks, 1):
        title = SVG_TITLE.search(block)
        name = title.group(1).strip()[:48] if title else f"figure {index}"
        try:
            ET.fromstring(block)
        except ET.ParseError as error:
            findings.append(f"figure {index} ({name}) is not well formed: {error}")
            continue
        missing = sorted(set(REF.findall(block)) - set(ID.findall(block)))
        if missing:
            findings.append(
                f"figure {index} ({name}) points at {', '.join(missing)}, "
                "which no id in the same svg defines; the arrowheads vanish "
                "with no error"
            )
    return len(blocks), findings


def check_figures(view):
    """(verdict, findings). The hook owns the width rules; this only runs it."""
    if not (os.path.isfile(FIGURE_HOOK) and os.access(FIGURE_HOOK, os.X_OK)):
        # An absent guard is not a passing guard. Printing the absence and
        # returning no finding ended the run `VERDICT ok`, exit 0, so a lost
        # file or a lost execute bit read exactly like three rules checked.
        return ("missing", [f"the figure guard is not runnable at {FIGURE_HOOK}, "
                            "so no figure was checked against svg-rules.md"])
    done = subprocess.run([FIGURE_HOOK, view], capture_output=True, text=True)
    if done.returncode == 0:
        return ("ok", [])
    # The hook frames its findings with a banner and a pointer line. Only the
    # lines carrying a file position are findings, and counting the frame
    # would report three failures for one bad figure.
    findings = [line.strip() for line in done.stderr.splitlines() if HOOK_FINDING.search(line)]
    return ("failed", findings or ["check-figures exited non-zero with no finding line"])


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 2
    view = os.path.abspath(argv[0])
    if not os.path.isfile(view):
        fail(f"no view at {view}")

    scratch = None
    rest = argv[1:]
    if rest[:1] == ["--out"]:
        if len(rest) < 2:
            fail("--out needs a directory")
        scratch = os.path.abspath(rest[1])
        os.makedirs(scratch, exist_ok=True)
    elif rest:
        fail(f"unknown argument {rest[0]}")
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="render-check-")

    chrome = find_chrome()
    if chrome is None:
        fail("no Chrome or Chromium found; install one or render by hand")

    failures = []
    notes = []
    with open(view, encoding="utf-8") as handle:
        source = handle.read()
    measured = layout_width(chrome, scratch, NARROW)
    for label, width in (("wide", WIDE), ("narrow", NARROW)):
        png = os.path.join(scratch, f"{label}.png")
        if not shoot(chrome, view, png, width):
            failures.append(f"{label} render wrote no image")
            continue
        got, height, whole = trim(png)
        if got is None:
            print(f"{label:7} {png}  {width} wide, tail not trimmed")
            notes.append(
                "Pillow is not installed, so neither image was trimmed and "
                "neither was checked for reaching the end of the page"
            )
            continue
        note = "" if whole else "  PAGE IS TALLER THAN THE CAPTURE"
        effective = measured if label == "narrow" and measured else width
        print(f"{label:7} {png}  {got}x{height}, laid out at {effective}{note}")
        if not whole:
            failures.append(f"{label} render did not reach the end of the page")

        scroll, inner = sideways(chrome, scratch, source, width, label)
        if scroll is None:
            notes.append(f"the {label} width carried no overflow measurement")
        elif scroll > inner:
            failures.append(
                f"the page scrolls sideways at {inner} units: its content is "
                f"{scroll} wide, so {scroll - inner} units sit off the right "
                "edge. An unbreakable token in a grid or a table is the usual "
                "cause"
            )
            print(f"        overflow: scrollWidth {scroll} over viewport {inner}")

    if measured and measured != NARROW:
        print(f"note    narrow render asked for {NARROW} and got {measured}")

    page_findings = check_page(source)
    print(f"page    {'ok' if not page_findings else 'failed'}")
    for finding in page_findings:
        print(f"        {finding}")
    failures.extend(page_findings)

    count, svg_findings = check_svg(source)
    print(f"svg     {count} figure(s), {'ok' if not svg_findings else 'failed'}")
    for finding in svg_findings:
        print(f"        {finding}")
    failures.extend(svg_findings)

    verdict, hook_findings = check_figures(view)
    print(f"figures {verdict}")
    for finding in hook_findings:
        print(f"        {finding.strip()}")
    failures.extend(hook_findings)

    notes = list(dict.fromkeys(notes))  # both renders raise the same one
    tail = f" ({len(notes)} note)" if notes else ""
    print(f"VERDICT {'ok' if not failures else str(len(failures)) + ' failing'}{tail}")
    for note in notes:
        print(f"        note: {note}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
