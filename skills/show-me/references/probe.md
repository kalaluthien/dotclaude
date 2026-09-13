# The 320 px probe

The command below ran as written on macOS. Copy it; do not retype from
memory. `<page>` is the absolute path of the page, written before the probe.

A screenshot cannot show a sideways page scroll at 320 px: headless Chrome here lays a page out at no less than 500 px whatever
`--window-size` says, then crops the PNG. An iframe is a true 320 px viewport,
media queries included. Run this before any delivery of an HTML page.

```sh
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p /tmp/show-me-shot          # Chrome exits 0 and writes nothing without it
cat >| /tmp/show-me-shot/frame.html <<'EOF'
<iframe id=f src="file://<page>" style="width:320px;height:800px;border:0"></iframe>
<script>f.onload=function(){var d=f.contentDocument.documentElement;document.body.dataset.r=d.scrollWidth+'/'+d.clientWidth}</script>
EOF
"$CHROME" --headless --disable-gpu --allow-file-access-from-files --dump-dom \
  --virtual-time-budget=3000 file:///tmp/show-me-shot/frame.html | grep -o 'data-r="[^"]*"'
```

It passes when the two numbers are equal (`305/305`: the frame's scrollbar
takes 15). A wide figure left outside its own scroll box reads `592/305`.
Without `--allow-file-access-from-files` the frame is unreadable and nothing
is printed, which is not a pass.
