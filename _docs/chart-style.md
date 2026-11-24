# Chart style

This guide is for us. It is not part of the website. Every chart on the blog follows these rules, so the posts look like one collection. The picture `chart-style-sample.png` in this folder shows all of them on one sheet.

## The four rules

1. The paper is cream (`#F4EDDD`) and the ink is warm black (`#2A2622`). They never change.
2. A chart that shows one thing uses ink and the sleeve colour of its post.
3. A chart that has to tell several things apart uses the five chart colours, always in the same order.
4. Text is always ink. No label takes the colour of its line or bar.

## Colours

The sleeve colour of a post is `--s1`. A post sets it with `sleeve:` in its header, and the chart picks it up by itself.

The five chart colours, in their fixed order:

| Order | Name | Value |
|---|---|---|
| 1 | teal | `#008F87` |
| 2 | red | `#C8452F` |
| 3 | blue | `#3F6DBF` |
| 4 | mustard | `#AD780A` |
| 5 | plum | `#B5578F` |

The first thing in a chart is teal, the second is red, and so on. A thing keeps its colour in every chart of a post. A chart with more than five things gets split into several small charts.

For amounts that go from little to much, use one colour from light to dark: `#8BA8DD`, `#688DD3`, `#4A74C5`, `#335CA9` and `#1F3F7C`.

These colours are not in the site's stylesheet. The first post that needs them adds them to `theme.scss`.

These colours are a little stronger than the dusty sleeve colours. The dusty ones did not pass the check below: two read as grey, and one was too pale on cream.

## Marks

| Mark | Class | Use it for |
|---|---|---|
| Solid line, 2 pixels | `line` | The main line, or the range of a value |
| Dotted line | `dots` | A comparison |
| Dashed line | `dash` | A reference value, such as an average |
| Dot with an ink outline | `dot` | A measured value, in the sleeve colour |
| Soft fill | `tint` | A range, in the sleeve colour |
| Grey bar | none yet | A bar that is not the highlight: ink at 28% strength |
| Thin grey line | `thin` | Grid lines and the baseline |
| Paper coloured outline | none yet | Marks that overlap: a 2 pixel outline in the paper colour |

## Text

Names of things, such as countries, are set in Fraunces with the class `name`. Numbers, axis labels and legends are set in IBM Plex Sans. Axis labels take the class `quiet`.

Write a number next to a mark only where the reader needs it, such as the highest and the lowest value. The other numbers appear when the reader points at a mark.

A chart with two or more things names each one, at the end of its line or in a legend under the chart.

## How a chart is made

A chart is drawn as part of the page, so it uses the page's typeface and colours. The first post shows the pattern:

1. `posts/soulmates/chart_data.json` holds the numbers and says where they come from.
2. `posts/soulmates/charts.py` draws each chart from those numbers and writes one small file per chart.
3. The post includes that file where the chart belongs.

Run it in the post's folder:

```bash
python3 charts.py
```

The script ends with a check that the numbers in the data file are the ones the post states in its text.

## Checking new colours

The five chart colours and the ramp were tested against the cream paper. The test asks four things:

1. Is the colour neither too light nor too dark?
2. Does it read as a colour and not as grey?
3. Can readers who cannot tell red from green still tell neighbours apart?
4. Does it stand out from the paper?

A new colour has to pass the same test before it joins the list.
