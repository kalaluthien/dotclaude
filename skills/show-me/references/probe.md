# The 320 px probe

Run it before any delivery of an HTML page. The command below ran as written
on macOS; copy it, do not retype from memory. `<page>` is the absolute path of
the page, `<dir>` the session's scratchpad directory, `/tmp` where none is
named.

A screenshot cannot show a sideways page scroll at 320 px: headless Chrome
here lays a page out at no less than 500 px whatever `--window-size` says,
then crops the PNG. An iframe is a true 320 px viewport, media queries
included.

```sh
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p <dir>/show-me-probe        # the redirect below fails without it
cat >| <dir>/show-me-probe/frame.html <<'EOF'
<iframe id=f src="file://<page>" style="width:320px;height:800px;border:0"></iframe>
<script>f.onload=function(){var w=f.contentWindow,d=w.document,e=d.documentElement,t=d.createTreeWalker(d.body,4),n,p,m,s=1/0,c,x=0;
while(n=t.nextNode()){p=n.parentElement;if(!n.data.trim()||/^(script|style|title)$/i.test(p.tagName))continue;m=p.getScreenCTM&&p.getScreenCTM();s=Math.min(s,parseFloat(w.getComputedStyle(p).fontSize)*(m?Math.hypot(m.a,m.b):1))}
var r=e.scrollWidth+'/'+e.clientWidth+' '+s.toFixed(1)+'px';c=d.querySelectorAll('button,summary');
c.forEach(function(b){var h=e.outerHTML;b.click();if(e.outerHTML==h)x++});document.body.dataset.r=r+' '+x+'/'+c.length}</script>
EOF
"$CHROME" --headless --disable-gpu --allow-file-access-from-files --dump-dom \
  --virtual-time-budget=3000 file://<dir>/show-me-probe/frame.html | grep -o 'data-r="[^"]*"'
```

It prints `<scroll>/<client> <smallest>px <dead>/<controls>`, as
`320/320 12.0px 0/1`, and passes on all three:

- **Width**: the two numbers are equal; a 600 px figure left outside its own
  scroll box reads `608/320`.
- **Legibility**: the smallest text, its font size times the scale of the SVG
  it sits in, is 11 px or more.
- **Controls**: the dead count is 0: every button and summary, clicked once,
  changed the page.

Without `--allow-file-access-from-files` the frame is unreadable and nothing
is printed, which is not a pass.
