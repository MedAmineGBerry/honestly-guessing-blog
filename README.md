# Honestly Guessing

Honestly Guessing is my blog. I try to investigate sayings, common ideas and other things people repeat, and check what the data says about them. You will also find my talks here.

When the site is switched on, it is at <https://medaminegberry.github.io/honestly-guessing-blog/>.

## Posts

| Op. | Saying | Verdict | Code |
|---|---|---|---|
| 1 | Is there really only one? | About fourteen | [soulmates](https://github.com/MedAmineGBerry/soulmates) |

## Look at it on your machine

The site is built with Quarto. Quarto comes with this folder through uv, so nothing has to be installed on the system.

```bash
uv run quarto preview
```

The preview opens in the browser and reloads when a file changes.

## Write a new post

1. Make a new folder under `posts/` and put an `index.qmd` in it. Images go next to it.
2. Fill in the header:

```yaml
---
title: "Do opposites attract?"
subtitle: "One line on how it was measured."
description: "Two sentences for search results and link previews."
date: 2027-01-15
opus: 2
verdict: "Not really"
sleeve: teal
---
```

`opus` is the number of the post. `verdict` is two or three words for the round sticker. `sleeve` is the colour of the post: `mustard`, `sunset`, `teal`, `rose`, `blue` or `pastel`.

3. Add a row to the table of posts in this file.

## Publish

The source of the blog lives on the branch `main`. The finished site lives on a second branch, `gh-pages`, and GitHub serves that branch. One command renders the site and pushes it there:

```bash
uv run quarto publish gh-pages --no-browser
```

It asks once for a yes. The site updates one or two minutes later.

Saving your work is a separate step, with the usual `git add`, `git commit` and `git push` on `main`. The rendered folder `docs/` is not committed.

## Turn the site on and off

The site is on while the branch `gh-pages` exists on GitHub. So the switch is two plain git commands, and no extra tool is needed.

Switch it on. This is the publish command from above:

```bash
uv run quarto publish gh-pages --no-browser
```

Switch it off. This deletes the published copy on GitHub and nothing else:

```bash
git push origin --delete gh-pages
```

Switching off takes the web pages offline. Your posts and all source files stay safe on `main`. The repository itself stays public on GitHub. To hide that as well, make the repository private under Settings.

If the site does not react, look at Settings, then Pages, on GitHub. The branch there should read `gh-pages`. To force the site off by hand, open the three dots next to "Your site is live at" and choose "Unpublish site".

## How it is put together

| File | What it does |
|---|---|
| `_quarto.yml` | Site settings. The output goes to `docs/`. |
| `theme.scss` | The look: cream paper, warm ink, the six sleeve colours. |
| `listing.ejs` | The home page, one row per post. |
| `posts/title-block.html` | The header of a post, with the verdict sticker. |
| `fonts/` | Fraunces and IBM Plex Sans, served from this site. |
| `docs/` | The rendered site on your machine. It is not committed. |

The pages load nothing from other servers. The design decisions are written down in `_docs/superpowers/specs/2026-11-12-blog-design.md`.

## Data and licences

Each post lists its data sources and their licences at its end.
