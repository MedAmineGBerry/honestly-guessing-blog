# Honestly Guessing

A blog that takes a saying everybody knows and checks it against data. Each post states its guesses in the open, shows where every number comes from and links to code you can run. Talks and their decks live inside the posts.

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

## Publish a change

GitHub serves the folder `docs/` as it is. No build runs on GitHub, so render before you commit.

```bash
uv run quarto render
```

```bash
git add -A
```

```bash
git commit -m "Describe the change"
```

```bash
git push
```

The site updates one or two minutes after the push.

## Turn the site on and off

Switching the site off takes the web pages offline. The repository and its files stay public on GitHub. To hide those as well, make the repository private under Settings.

### In the browser

To switch it off, open the repository on GitHub, then Settings, then Pages. Next to "Your site is live at", open the menu with the three dots and choose "Unpublish site".

To switch it on, open Settings, then Pages. Under "Build and deployment" choose "Deploy from a branch", the branch `main` and the folder `/docs`, and save. GitHub publishes again with the next push. If there is nothing new to push, send an empty commit:

```bash
git commit --allow-empty -m "Publish the site again"
```

```bash
git push
```

### From the terminal

This needs the GitHub command line tool `gh`. Log in once with `gh auth login`.

Switch it off:

```bash
gh api -X DELETE repos/MedAmineGBerry/honestly-guessing-blog/pages
```

Switch it on:

```bash
gh api -X POST repos/MedAmineGBerry/honestly-guessing-blog/pages -f "source[branch]=main" -f "source[path]=/docs"
```

Check the state. The answer is `built` when the site is on, `building` while GitHub prepares it, and an error "Not Found" when it is off.

```bash
gh api repos/MedAmineGBerry/honestly-guessing-blog/pages --jq .status
```

If the state stays empty after switching on, send the empty commit from above.

## How it is put together

| File | What it does |
|---|---|
| `_quarto.yml` | Site settings. The output goes to `docs/`. |
| `theme.scss` | The look: cream paper, warm ink, the six sleeve colours. |
| `listing.ejs` | The home page, one row per post. |
| `posts/title-block.html` | The header of a post, with the verdict sticker. |
| `fonts/` | Fraunces and IBM Plex Sans, served from this site. |
| `docs/` | The rendered site. Do not edit it by hand. |

The pages load nothing from other servers. The design decisions are written down in `_docs/superpowers/specs/2026-11-12-blog-design.md`.

## Data and licences

Each post lists its data sources and their licences at its end.
