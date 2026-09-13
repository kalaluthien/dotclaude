# Rendering a show-me page to PNG, and probing its widths

Every command below ran as written on macOS. Copy them; do not retype from
memory.

## The 320 px probe

A screenshot cannot show a sideways page scroll at 320 px: headless Chrome here lays a page out at no less than 500 px whatever
`--window-size` says, then crops the PNG. An iframe is a true 320 px viewport,
media queries included. Run this before any delivery of an HTML page.

```sh
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p /tmp/show-me-shot          # Chrome exits 0 and writes nothing without it
cat >| /tmp/show-me-shot/frame.html <<'EOF'
<iframe id=f src="file:///tmp/show-me-<slug>.html" style="width:320px;height:800px;border:0"></iframe>
<script>f.onload=function(){var d=f.contentDocument.documentElement;document.body.dataset.r=d.scrollWidth+'/'+d.clientWidth}</script>
EOF
"$CHROME" --headless --disable-gpu --allow-file-access-from-files --dump-dom \
  --virtual-time-budget=3000 file:///tmp/show-me-shot/frame.html | grep -o 'data-r="[^"]*"'
```

It passes when the two numbers are equal (`305/305`: the frame's scrollbar
takes 15). A wide figure left outside its own scroll box reads `592/305`.
Without `--allow-file-access-from-files` the frame is unreadable and nothing
is printed, which is not a pass.

## The PNG for a phone

Shoot taller than the page, then trim to the last row that differs from the
background — Chrome has no full-page flag here.

```sh
"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --screenshot=/tmp/show-me-shot/tall.png --window-size=900,6000 \
  "file:///tmp/show-me-<slug>.html"
```

`python3` off PATH has PIL; `/usr/bin/python3` does not.

```python
from PIL import Image
im = Image.open('/tmp/show-me-shot/tall.png').convert('RGB')
w, h = im.size
bg = im.getpixel((5, h - 5))
px = im.load()
last = next(y for y in range(h - 1, -1, -1)
            if any(px[x, y] != bg for x in range(0, w, 7)))
im.crop((0, 0, w, last + 40)).save('/tmp/show-me-shot/page.png')
```

**Check that the trim height is well under the window height.** Chrome silently
crops at `--window-size`, and the trimmed result then looks exactly like a
correctly-trimmed shorter page: a 7147-tall page shot at
`--window-size=900,7000` trimmed to 7029 and lost its last section with no
error. When `last` lands within ~100 units of the window height, re-shoot
taller.

Then split into `round(height / 950)` slices and Read each. 950 units is one
comfortable phone screen; a single full-page image arrives unreadable. Four is
not a constant -- a 7000-unit page needs seven.
