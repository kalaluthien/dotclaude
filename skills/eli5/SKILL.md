---
name: eli5
description: Explain a topic to someone who knows nothing about it, as an HTML page of big pictures and few words. Use when the user types /eli5 <topic>.
disable-model-invocation: true
---

# eli5

Explain the topic as if to someone who has never heard of it. Big pictures, few words: every idea earns a drawing, and the words beside it are the caption, not the explanation. If the user typed no topic, explain whatever the conversation is currently about.

Write one self-contained HTML page to `/tmp/eli5-<topic-slug>.html` — inline styles and inline SVG only, nothing fetched from the network, so it opens with no connection. Then deliver it both ways — `open` on that path for the desktop, and SendUserFile (display: render) for a phone — and tell the user the one-sentence version in chat.

Topic: $ARGUMENTS
