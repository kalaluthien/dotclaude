# Rendering an eli5 page to PNG for a phone

Every command below ran successfully on 2026-09-01 (macOS, Chrome 900-unit
window). Copy them; do not retype from memory.

`~/.claude/skills/writing/scripts/render-check.py` is the wrong tool for
this: it caps the capture at 16000 units and reports `PAGE IS TALLER THAN THE
CAPTURE` for a page that is in fact 3785 tall, and it fails an eli5 page on the
`<dl class="provenance">` rule that only a `docs/` view carries.

Shoot taller than the page, then trim to the last row that differs from the
background — Chrome has no full-page flag here.

```sh
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --screenshot=/tmp/eli5-shot/tall.png --window-size=900,6000 \
  "file:///tmp/eli5-<slug>.html"
```

`python3` off PATH has PIL; `/usr/bin/python3` does not.

```python
from PIL import Image
im = Image.open('/tmp/eli5-shot/tall.png').convert('RGB')
w, h = im.size
bg = im.getpixel((5, h - 5))
px = im.load()
last = next(y for y in range(h - 1, -1, -1)
            if any(px[x, y] != bg for x in range(0, w, 7)))
im.crop((0, 0, w, last + 40)).save('/tmp/eli5-shot/page.png')
```

**Check that the trim height is well under the window height.** Chrome silently
crops at `--window-size`, and the trimmed result then looks exactly like a
correctly-trimmed shorter page. On 2026-09-03 a 7147-tall page shot at
`--window-size=900,7000` trimmed to 7029 and lost its last section with no
error. When `last` lands within ~100 units of the window height, re-shoot
taller.

Then split into `round(height / 950)` slices and Read each. 950 units is one
comfortable phone screen; a single full-page image arrives unreadable. Four is
not a constant -- a 7000-unit page needs seven.
