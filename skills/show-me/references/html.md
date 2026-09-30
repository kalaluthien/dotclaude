# HTML page rules

Read when making a temporary page. Write the file in the scratchpad and send it with `SendUserFile`; never open it in a browser.

## Page

- Write one complete, self-contained HTML file: inline CSS, no external requests, no CDN links, no web fonts, so it renders with the network off.
- Include `<meta charset="utf-8">`, or every apostrophe turns to gibberish.
- Read the file back yourself before you describe it.
- No background grid or texture on anything text-heavy, since it makes a dense document hard to read.

## The PICK board

Plain on purpose, so the options carry all the visual weight; each card's button copies the pick, so they answer by clicking.

```html
<!doctype html><meta charset="utf-8"><title>Pick a direction</title>
<style>
 :root{--bg:#fff;--fg:#14171a;--mut:#5d6b7a;--line:#e3e8ef;--card:#f7f9fb;--accent:#c2410c}
 @media (prefers-color-scheme:dark){
   :root{--bg:#0f1418;--fg:#eef2f6;--mut:#9aa8b6;--line:#243039;--card:#161d23;--accent:#fb923c}}
 *{box-sizing:border-box}
 body{margin:0;background:var(--bg);color:var(--fg);padding:40px 32px 80px;
      font:16px/1.55 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif}
 h1{font-size:26px;margin:0 0 6px}
 p.lede{margin:0 0 30px;color:var(--mut);max-width:70ch}
 .grid{display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
 .card{border:1px solid var(--line);border-radius:12px;background:var(--card);
       padding:18px;display:flex;flex-direction:column;gap:10px}
 .card img,.card svg{width:100%;display:block;border-radius:7px;border:1px solid var(--line)}
 h2{font-size:17px;margin:0}
 .angle{color:var(--mut);font-size:14px;margin:0;flex:1}
 button{font:inherit;font-size:14px;padding:9px 14px;border-radius:7px;cursor:pointer;
        border:1px solid var(--accent);background:transparent;color:var(--accent)}
 button:hover{background:var(--accent);color:var(--bg)}
</style>
<h1>Pick a direction</h1>
<p class="lede">One line on what to judge, and what to ignore.</p>
<div class="grid">
  <div class="card">
    <!-- the render: an inline <svg>, or live HTML -->
    <h2>A &mdash; name of the device</h2>
    <p class="angle">The argument this one makes, in one line.</p>
    <button onclick="navigator.clipboard.writeText('A');this.textContent='Copied — paste it back'">Pick A</button>
  </div>
  <!-- B and C the same -->
</div>
```

- Name the device, not the decoration: "timeline down the left" is a device, "blue version" means you built the same thing twice.
- Draw every image inline as SVG or HTML; a linked local file breaks the moment it moves.
- Judging shape: render it greyscale and say so in the lede, since colour decides the argument before they see the structure.

## Seen

A command that exits 0 proves it ran, not that they saw it: after `SendUserFile`, check it reports the file sent.
