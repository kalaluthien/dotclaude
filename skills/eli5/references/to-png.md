# Rendering an eli5 page to PNG for a phone

Every command below ran successfully on 2026-09-01 (macOS, Chrome 900-unit
window). Copy them; do not retype from memory.

`~/workspace/.claude/skills/writing/scripts/render-check` is the wrong tool for
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

Then split into four equal slices and Read each. Slices land near 950 units,
which is one comfortable phone screen; a single 3800-unit image arrives
unreadable.
