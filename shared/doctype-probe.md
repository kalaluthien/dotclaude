# The 320 px probe

Run it before any delivery of an HTML page, show-me's or grill-me's. The command below ran as written
on macOS; copy it, do not retype from memory. `<page>...` is the absolute path
of each page, any number of them, `<dir>` the session's scratchpad directory,
`/tmp` where none is named.

A screenshot cannot show a sideways page scroll at 320 px: headless Chrome
here lays a page out at no less than 500 px whatever `--window-size` says,
then crops the PNG. An iframe is a true 320 px viewport, media queries
included.

```sh
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FLOOR=$(grep -o 'under [0-9]* px' ~/.claude/shared/doctype.md | tr -dc '0-9\n' | paste -sd, -)
mkdir -p <dir>/doctype-probe        # the redirect below fails without it
cat >| <dir>/doctype-probe/frame.html <<'EOF'
<iframe id=f style="width:320px;height:800px;border:0"></iframe>
<script>f.onload=function(){var w=f.contentWindow,d=w.document,e=d.documentElement,t=d.createTreeWalker(d.body,4),X=d.createElement('canvas').getContext('2d'),n,p,m,z,s=[1/0,1/0],x=0,v=0,i=0,q=0;
while(n=t.nextNode()){p=n.parentElement;if(!n.data.trim()||/^(script|style|title)$/i.test(p.tagName))continue;m=p.getScreenCTM&&p.getScreenCTM();z=/[\p{sc=Hangul}\p{sc=Han}]/u.test(n.data)?1:0;s[z]=Math.min(s[z],parseFloat(w.getComputedStyle(p).fontSize)*(m?Math.hypot(m.a,m.b):1))}
d.querySelectorAll('[aria-labelledby],[aria-describedby]').forEach(function(q){((q.getAttribute('aria-labelledby')||'')+' '+(q.getAttribute('aria-describedby')||'')).trim().split(/\s+/).forEach(function(k){if(d.querySelectorAll('[id="'+k+'"]').length!=1)i++})});
d.querySelectorAll('[src],link[rel~=stylesheet]').forEach(function(u){if(!/^data:/i.test(u.getAttribute('src')||u.getAttribute('href')||''))q++});
var F=location.search.slice(1).split(','),c=d.querySelectorAll('button,summary'),r=e.scrollWidth+'/'+e.clientWidth+' '+s.map(function(u){return u<1/0?u.toFixed(1)+'px':'-'}).join(' '),k=e.scrollWidth==e.clientWidth&&s[0]>=F[0]&&s[1]>=F[1]&&!i&&!q;
c.forEach(function(b){var h=e.outerHTML;b.click();if(e.outerHTML==h)x++});var y=c.length;
d.querySelectorAll('figure').forEach(function(g){if(g.scrollWidth>g.clientWidth){y++;g.focus();if(g.tabIndex<0||w.getComputedStyle(g).outlineStyle=='none')x++}});
d.querySelectorAll('details').forEach(function(q){q.open=true});
d.querySelectorAll('svg').forEach(function(g){var o=g.getBoundingClientRect(),u=0;g.querySelectorAll('rect,circle,ellipse,line,polyline,polygon,path,text,image,use').forEach(function(q){var b=q.getBoundingClientRect(),a=0,j=0,M,h;if(q.closest('defs,marker,clipPath,mask,symbol,pattern')||!b.width&&!b.height)return;
if(q.tagName=='text'){X.font=w.getComputedStyle(q).font;M=X.measureText(q.textContent);h=b.height/(M.fontBoundingBoxAscent+M.fontBoundingBoxDescent);a=(M.fontBoundingBoxAscent-M.actualBoundingBoxAscent)*h;j=(M.fontBoundingBoxDescent-M.actualBoundingBoxDescent)*h}
if(b.left<o.left-.5||b.right>o.right+.5||b.top+a<o.top-.5||b.bottom-j>o.bottom+.5)u=1});v+=u});document.body.dataset.r=r+' '+x+'/'+y+' clip '+v+' id '+i+' ext '+q+' floor '+F+(k&&!x&&!v?' pass':' FAIL')};f.src=location.hash.slice(1)</script>
EOF
for P in <page>...; do
  R=$("$CHROME" --headless --disable-gpu --allow-file-access-from-files --dump-dom \
    --virtual-time-budget=3000 "file://<dir>/doctype-probe/frame.html?$FLOOR#file://$P" 2>/dev/null |
    sed -n 's/.*data-r="\([^"]*\)".*/\1/p')
  echo "$P ${R:-no reading FAIL}"
done
```

It prints one line per page: the page, then `<scroll>/<client> <smallest>px
<smallest Hangul or Han>px <dead>/<controls> clip <n> id <n> ext <n> floor
<px>,<px>` and the verdict, as
`/abs/page.html 320/320 12.0px 13.0px 0/1 clip 0 id 0 ext 0 floor 11,12 pass`;
`-` stands where a page has no text of that kind. `pass` needs each of these:

- **Width**: the two numbers are equal; a figure wider than the frame, left
  outside its own scroll box, reads more on the left.
- **Legibility**: the smallest text, its font size times the scale of the SVG
  it sits in, is at least its script's floor: a text node holding Hangul or
  Han the second, every other the first, both read from
  `~/.claude/shared/doctype.md` § Page: Legible. A floor with one number or
  none means a line was not found, and fails, as it does from a checkout whose
  `shared/` the install does not have yet: point `FLOOR` at the checkout's copy
  there.
- **Controls**: the dead count is 0: every button and summary, clicked once,
  changed the page, and every figure that scrolls sideways has a `tabindex`
  and no `outline: none` when focused. Chrome focuses a scroller without a
  `tabindex`; Safari does not.
- **Clip**: 0 SVGs with a shape or a text past the SVG's own box on screen,
  which is what it shows whatever its `viewBox` says; every `details` is
  opened first, so a closed one's figures are read too. A text is measured by
  its glyphs' ink (canvas `measureText`), a shape by its geometry: Chrome's
  boxes leave out strokes and markers and ignore `getBBox`'s options to add
  them, so a stroke or an arrowhead past the edge is not read.
- **Id**: 0 `aria-labelledby` or `aria-describedby` ids naming anything but
  exactly one element; two inline SVGs share one id space.
- **Ext**: 0 elements whose `src`, or stylesheet link whose `href`, is not a
  `data:` URI: § Page: One file fetches nothing.

A page the frame cannot read -- a wrong path, or no
`--allow-file-access-from-files` -- prints `no reading FAIL`.
