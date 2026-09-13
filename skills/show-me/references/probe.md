# The 320 px probe

Run it before any delivery of an HTML page. The command below ran as written
on macOS; copy it, do not retype from memory. `<page>...` is the absolute path
of each page, any number of them, `<dir>` the session's scratchpad directory,
`/tmp` where none is named.

A screenshot cannot show a sideways page scroll at 320 px: headless Chrome
here lays a page out at no less than 500 px whatever `--window-size` says,
then crops the PNG. An iframe is a true 320 px viewport, media queries
included.

```sh
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FLOOR=$(sed -n 's/.*no text under \([0-9]*\) px.*/\1/p' ~/.claude/types/doctype.md)
mkdir -p <dir>/show-me-probe        # the redirect below fails without it
cat >| <dir>/show-me-probe/frame.html <<'EOF'
<iframe id=f style="width:320px;height:800px;border:0"></iframe>
<script>f.onload=function(){var w=f.contentWindow,d=w.document,e=d.documentElement,t=d.createTreeWalker(d.body,4),n,p,m,s=1/0,c,x=0;
while(n=t.nextNode()){p=n.parentElement;if(!n.data.trim()||/^(script|style|title)$/i.test(p.tagName))continue;m=p.getScreenCTM&&p.getScreenCTM();s=Math.min(s,parseFloat(w.getComputedStyle(p).fontSize)*(m?Math.hypot(m.a,m.b):1))}
var F=parseFloat(location.search.slice(1)),r=e.scrollWidth+'/'+e.clientWidth+' '+s.toFixed(1)+'px',k=e.scrollWidth==e.clientWidth&&s>=F;c=d.querySelectorAll('button,summary');
c.forEach(function(b){var h=e.outerHTML;b.click();if(e.outerHTML==h)x++});document.body.dataset.r=r+' '+x+'/'+c.length+' floor '+F+(k&&!x?' pass':' FAIL')};f.src=location.hash.slice(1)</script>
EOF
for P in <page>...; do
  R=$("$CHROME" --headless --disable-gpu --allow-file-access-from-files --dump-dom \
    --virtual-time-budget=3000 "file://<dir>/show-me-probe/frame.html?$FLOOR#file://$P" 2>/dev/null |
    sed -n 's/.*data-r="\([^"]*\)".*/\1/p')
  echo "$P ${R:-no reading FAIL}"
done
```

It prints one line per page: the page, then `<scroll>/<client> <smallest>px
<dead>/<controls> floor <px>` and the verdict, as
`/abs/page.html 320/320 12.0px 0/1 floor 11 pass`. `pass` needs all three:

- **Width**: the two numbers are equal; a figure wider than the frame, left
  outside its own scroll box, reads more on the left.
- **Legibility**: the smallest text, its font size times the scale of the SVG
  it sits in, is at least the floor, read from `~/.claude/types/doctype.md`
  § Page: Legible; `floor NaN` means that line was not found, and fails, as it
  does from a checkout whose `types/` the install does not have yet: point
  `FLOOR` at the checkout's copy there.
- **Controls**: the dead count is 0: every button and summary, clicked once,
  changed the page.

A page the frame cannot read -- a wrong path, or no
`--allow-file-access-from-files` -- prints `no reading FAIL`.
