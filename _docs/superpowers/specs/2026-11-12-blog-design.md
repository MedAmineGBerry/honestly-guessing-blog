# Honestly Guessing: blog design

A personal blog on GitHub Pages. Each post takes a saying, tests it with data and links to a repository with the code. The first post is the soul mates project.

This note lives in `_docs/` and not in `docs/`. Quarto skips folders that start with an underscore, and `docs/` holds the rendered site.

## Decisions

| Topic | Decision |
|---|---|
| Tool | Quarto 1.11, installed in this folder through uv as the dev dependency `quarto-cli`. Nothing is installed on the system. |
| Repository | `MedAmineGBerry/honestly-guessing-blog` on GitHub, a project site. The address is `https://medaminegberry.github.io/honestly-guessing-blog/`. The local folder is still named `MedAmineGBerry.github.io`. Every link and font path in the site is relative, so the site works under any address. |
| Publishing | The source lives on `main`. `uv run quarto publish gh-pages` renders the site into `docs/` and pushes it to the branch `gh-pages`, which GitHub Pages serves. `docs/` is not committed. No build runs on GitHub. |
| On and off | The site is on while the branch `gh-pages` exists on GitHub. Publishing switches it on. `git push origin --delete gh-pages` switches it off. The owner wanted a switch that needs no tool besides git. |
| Look | A record sleeve: cream paper, warm ink, three stripes under the site name and a round sticker that carries the verdict. The blog has its own look and does not copy the soul mates deck. Titles and text are set in Fraunces, small labels in IBM Plex Sans capitals. |
| Colour | The paper and the ink never change. Each post picks one of six sleeve colours with `sleeve:` in its header: `mustard`, `sunset`, `teal`, `rose`, `blue` or `pastel`. Stripes, sticker and link underlines take that colour. Mustard is the house colour for pages that are not a post, and the colour of the first post. A new colour is one line in `theme.scss`. |
| Dark mode | None. The cream paper is the identity. |
| Fonts | The files live in `fonts/`. `theme.scss` points to them with a path relative to itself, and Quarto copies them next to the compiled stylesheet in `site_libs/bootstrap/fonts/`. The default Quarto theme loads nothing from other servers, so no reader's address goes to a font server. |
| Posts | One folder per post under `posts/`, with its images next to it. |
| Animations | A post mixes text with small animations, about one per idea. Each is a plain script in the post's folder, with no library and nothing from other servers. It takes its colour from the sleeve, starts on a button, has a slider, and hides the button for readers who switched motion off. The first one is `posts/soulmates/lives.js`. |
| Code | Each project keeps its own repository. A post links to it and may embed a deck or charts from it. |

## Files

```
_quarto.yml               # site config, output to docs/
theme.scss                # paper, ink, the six sleeve colours, all rules
listing.ejs               # home page: one row per post with stripes and sticker
posts/title-block.html    # post header: title, Op. number, verdict sticker
index.qmd                 # home: the list of posts
about.qmd                 # what the blog is
posts/_metadata.yml       # defaults for all posts
posts/soulmates/index.qmd # first post
posts/soulmates/img/      # four charts from the soulmates notebooks
posts/soulmates/deck.html # a copy of talk/soulmates_pycon.html
fonts/                    # three WOFF2 files: Fraunces normal and italic, IBM Plex Sans
pyproject.toml, uv.lock   # the uv project that provides Quarto
docs/                     # the rendered site, not committed
```

## Working on it

Render the site:

```bash
uv run quarto render
```

Preview it with live reload:

```bash
uv run quarto preview
```

A new post is a new folder under `posts/` with an `index.qmd`. Its header takes three fields next to the title and the date. `opus` is the number of the post. `verdict` is two or three words for the sticker. `sleeve` is the colour. A Jupyter notebook can be a post too. Put the `.ipynb` in its folder and give it a title and a date in a first raw cell.

## Going online, once

1. The public repository `honestly-guessing-blog` exists on GitHub. It started with a README commit.
2. Add it as the remote, pull its README commit once with `--allow-unrelated-histories`, then push `main`.
3. Run `uv run quarto publish gh-pages`. GitHub notices the new branch and switches Pages on for a project site.

## Open points

1. The post has no author line. The owner decides which name appears.
2. The embedded deck still shows two placeholders, for the speaker name and the repository link.
3. A site published from Germany may need an imprint. This is a legal question for the owner to check.
4. The French contact data has a "no derivatives" licence. The post shows results computed from it and credits it. Whether a chart counts as a derivative is a question for the owner to check.
