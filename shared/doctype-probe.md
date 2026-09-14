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
SKIN=~/.claude/shared/doctype-skin.css
mkdir -p <dir>/doctype-probe        # the redirects below fail without it
tr -d '\r' < "$SKIN" | sed 's/^[[:space:]]*//' >| <dir>/doctype-probe/skin.css   # empty when SKIN is missing
cat >| <dir>/doctype-probe/frame.html <<'EOF'
<iframe id=f style="width:320px;height:800px;border:0"></iframe>
<script>f.onload=function(){var w=f.contentWindow,d=w.document,e=d.documentElement,t=d.createTreeWalker(d.body,4),X=d.createElement('canvas').getContext('2d'),A=location.search.slice(1).split(';'),K=A[0],F=(A[1]||'').split(','),c=d.querySelectorAll('button,summary'),U={},n,p,m,z,s=[1/0,1/0],x=0,v=0,i=0,q=0,y=c.length;
c.forEach(function(b){var h=e.outerHTML;b.click();if(e.outerHTML==h)x++});
d.querySelectorAll('details').forEach(function(g){g.open=true});
while(n=t.nextNode()){p=n.parentElement;if(!n.data.trim()||/^(script|style|title)$/i.test(p.tagName))continue;m=p.getScreenCTM&&p.getScreenCTM();z=/[\p{sc=Hangul}\p{sc=Han}]/u.test(n.data)?1:0;s[z]=Math.min(s[z],parseFloat(w.getComputedStyle(p).fontSize)*(m?Math.hypot(m.a,m.b):1))}
d.querySelectorAll('[aria-labelledby],[aria-describedby]').forEach(function(g){((g.getAttribute('aria-labelledby')||'')+' '+(g.getAttribute('aria-describedby')||'')).trim().split(/\s+/).forEach(function(k){if(d.querySelectorAll('[id="'+k+'"]').length!=1)i++})});
var H=function(u){u=(u||'').trim();if(!u||u[0]=='#'||/^(data|about|blob):/i.test(u))return;try{u=new URL(u,d.baseURI).href}catch(_){}U[u]=1},C=function(t){t.replace(/url\(\s*(?:"((?:[^"\\]|\\.)*)"|'((?:[^'\\]|\\.)*)'|([^)\s]*))\s*\)|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'/gi,function(o,a,b,c){if(/^url/i.test(o))H((a||b||c||'').replace(/\\(.)/g,'$1'))})},R=function(l){[].forEach.call(l,function(u){if(u.type==10)return;if(u.type==3){H(u.href);try{R(u.styleSheet.cssRules)}catch(_){}}C(u.cssText);if(u.cssRules)R(u.cssRules)})};
w.performance.getEntriesByType('resource').forEach(function(u){H(u.name)});[].forEach.call(d.styleSheets,function(g){try{R(g.cssRules)}catch(_){}});
d.querySelectorAll('[src],[srcset],[poster],object[data],link[href],image[href],use[href],[style]').forEach(function(g){H(g.getAttribute('src'));H(g.getAttribute('poster'));if(/^(link|image|use)$/i.test(g.tagName))H(g.getAttribute('href'));if(g.tagName=='OBJECT')H(g.getAttribute('data'));(g.getAttribute('srcset')||'').replace(/[\t\n\f\r ,]*([^\t\n\f\r ]*[^\t\n\f\r ,])(?:,+|(?:[^,(]|\([^)]*\)?)*)/g,function(o,u){H(u)});if(g.style)C(g.style.cssText)});q=Object.keys(U).length;
var r=e.scrollWidth+'/'+e.clientWidth+' '+s.map(function(u){return u<1/0?u.toFixed(1)+'px':'-'}).join(' '),k=e.scrollWidth==e.clientWidth&&F.length==2&&s[0]>=F[0]&&s[1]>=F[1]&&!i&&!q&&K=='same';
d.querySelectorAll('body *').forEach(function(g){if(/auto|scroll/.test(w.getComputedStyle(g).overflowX)&&g.scrollWidth>g.clientWidth){y++;g.focus();if(g.tabIndex<0||w.getComputedStyle(g).outlineStyle=='none')x++}});
d.querySelectorAll('svg').forEach(function(g){var o=g.getBoundingClientRect(),u=0;g.querySelectorAll('rect,circle,ellipse,line,polyline,polygon,path,text,image,use').forEach(function(q){var b=q.getBoundingClientRect(),a=0,j=0,M,h;if(q.closest('defs,marker,clipPath,mask,symbol,pattern')||!b.width&&!b.height)return;
if(q.tagName=='text'){X.font=w.getComputedStyle(q).font;M=X.measureText(q.textContent);h=b.height/(M.fontBoundingBoxAscent+M.fontBoundingBoxDescent);a=(M.fontBoundingBoxAscent-M.actualBoundingBoxAscent)*h;j=(M.fontBoundingBoxDescent-M.actualBoundingBoxDescent)*h}
if(b.left<o.left-.5||b.right>o.right+.5||b.top+a<o.top-.5||b.bottom-j>o.bottom+.5)u=1});v+=u});document.body.dataset.r=r+' '+x+'/'+y+' clip '+v+' id '+i+' ext '+q+' skin '+K+' floor '+F+(k&&!x&&!v?' pass':' FAIL')};f.src=location.hash.slice(1)</script>
EOF
for P in <page>...; do
  K=differs
  tr -d '\r' < "$P" | sed -n '/\/\* skin:/,/\/\* skin end \*\//{s/^[[:space:]]*//;p;/\/\* skin end \*\//q;}' |
    cmp -s - <dir>/doctype-probe/skin.css && [ -s <dir>/doctype-probe/skin.css ] && K=same
  R=$("$CHROME" --headless --disable-gpu --allow-file-access-from-files --dump-dom \
    --virtual-time-budget=3000 "file://<dir>/doctype-probe/frame.html?$K;$FLOOR#file://$P" 2>/dev/null |
    sed -n 's/.*data-r="\([^"]*\)".*/\1/p')
  echo "$P ${R:-no reading FAIL}"
done
```

It prints one line per page: the page, then `<scroll>/<client> <smallest>px
<smallest Hangul or Han>px <dead>/<controls> clip <n> id <n> ext <n> skin
<same|differs> floor <px>,<px>` and the verdict, as
`/abs/page.html 320/320 12.0px 13.0px 0/1 clip 0 id 0 ext 0 skin same floor 11,12 pass`;
`-` stands where a page has no text of that kind. Every button and summary
is clicked first, then every `details` opened, and only then is the rest read.
`pass` needs each of these:

- **Width**: the two numbers are equal; a figure wider than the frame, left
  outside its own scroll box, reads more on the left.
- **Legibility**: the smallest text, its font size times the scale of the SVG
  it sits in, is at least its script's floor: a text node holding Hangul or
  Han the second, every other the first, both read from
  `~/.claude/shared/doctype.md` § Page: Legible. A floor of other than two
  numbers means a line was not found or was added, and fails; a missing
  `doctype-skin.css` reads `differs`. Both happen from a checkout whose
  `shared/` the install does not have yet: point `FLOOR` and `SKIN` at the
  checkout's copies there.
- **Controls**: the dead count is 0: every button and summary, clicked once,
  changed the page, and every box that scrolls sideways -- a figure, a
  table's box, a `pre` -- has a `tabindex` and no `outline: none` when
  focused. Chrome focuses a scroller without a
  `tabindex`; Safari does not.
- **Clip**: 0 SVGs with a shape or a text past the SVG's own box on screen,
  which is what it shows whatever its `viewBox` says. A text is measured by
  its glyphs' ink (canvas `measureText`), a shape by its geometry: Chrome's
  boxes leave out strokes and markers and ignore `getBBox`'s options to add
  them, so a stroke or an arrowhead past the edge is not read.
- **Id**: 0 `aria-labelledby` or `aria-describedby` ids naming anything but
  exactly one element; two inline SVGs share one id space.
- **Ext**: 0 URLs, other than `data:`, `about:`, `blob:` or a `#` fragment,
  among: every `src`, `poster` and `object` `data`; every `srcset` candidate,
  split on ASCII whitespace and commas as the spec splits it; the `href` of
  every `link` and every SVG `image` and `use`; every `url()` and `@import` in
  the style sheets, imported ones included, and in `style` attributes, read as
  the browser parsed them (`cssText`: no comments, strings skipped,
  `@namespace` aside); and what the page fetched before `load` (Resource
  Timing, which lists no `file://` fetch). The exemptions and the empty-value
  skip test the text as JS `trim()` leaves it, not the URL the browser parses;
  a URL that does not parse counts. § Page: One file fetches nothing. Any
  other shape is not read: an `xlink:href`, an `feImage` `href`, a legacy
  `background` attribute, a `link` `imagesrcset`, an SVG presentation
  attribute's `url()`, an SVG `script` `href`, a shadow root's content, a
  `meta` refresh, a URL a script builds, a nested frame's own fetches.
- **Skin**: `same`: the page carries `doctype-skin.css` verbatim, from its
  first `skin:` line to the `skin end` line after it, indentation and CR
  aside.

A page the frame cannot read -- a wrong path, or no
`--allow-file-access-from-files` -- prints `no reading FAIL`.
