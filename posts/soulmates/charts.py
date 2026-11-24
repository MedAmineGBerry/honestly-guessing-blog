"""Draw the three charts of the post from chart_data.json.

Run it in this folder with: python3 charts.py

Each chart is written as a small page fragment that the post includes. The pictures are part of the
page itself, so they use its typeface and the sleeve colour of the post. The look is set in theme.scss.
"""
import json
import math
import pathlib

HERE = pathlib.Path(__file__).parent
DATA = json.loads((HERE / "chart_data.json").read_text())


def figure(name, width, height, label, parts, caption):
    svg = f'<svg class="chart" viewBox="0 0 {width} {height}" role="img" aria-label="{label}">\n' + "\n".join(parts) + "\n</svg>"
    (HERE / f"_chart_{name}.html").write_text(f'<figure class="chart-fig">\n{svg}\n<figcaption>{caption}</figcaption>\n</figure>\n')


def countries():
    rows, typical = DATA["countries"], DATA["typical"]
    left, right, top, step, most = 146, 540, 46, 34, 13000
    x = lambda value: left + (right - left) * value / most
    bottom = top + step * (len(rows) - 1) + 17
    parts = []
    for tick in (0, 4000, 8000, 12000):
        parts.append(f'<line class="thin" x1="{x(tick):.1f}" y1="30" x2="{x(tick):.1f}" y2="{bottom}"/>')
        parts.append(f'<text class="quiet" x="{x(tick):.1f}" y="{bottom + 19}" text-anchor="middle">{tick:,}</text>')
    parts.append(f'<line class="dash" x1="{x(typical):.1f}" y1="24" x2="{x(typical):.1f}" y2="{bottom}"/>')
    parts.append(f'<text class="quiet" x="{x(typical):.1f}" y="15" text-anchor="middle">a typical country</text>')
    for i, row in enumerate(rows):
        y = top + step * i
        parts.append(f'<g><title>{row["name"]}: {row["mean"]:,} people, range {row["low"]:,} to {row["high"]:,}</title>')
        parts.append(f'<rect class="hit" x="0" y="{y - step / 2}" width="560" height="{step}"/>')
        parts.append(f'<text class="name" x="{left - 14}" y="{y + 5}" text-anchor="end">{row["name"]}</text>')
        parts.append(f'<line class="line" x1="{x(row["low"]):.1f}" y1="{y}" x2="{x(row["high"]):.1f}" y2="{y}"/>')
        parts.append(f'<circle class="dot" cx="{x(row["mean"]):.1f}" cy="{y}" r="5.5"/>')
        if i in (0, len(rows) - 1):  # only the highest and the lowest country carry their number
            parts.append(f'<text x="{x(row["high"]) + 9:.1f}" y="{y + 4.5}">{row["mean"]:,}</text>')
        parts.append("</g>")
    parts.append(f'<text class="quiet" x="{(left + right) / 2}" y="{bottom + 44}" text-anchor="middle">new people of your own age you talk to between 15 and 60</text>')
    first, last = rows[0], rows[-1]
    figure("countries", 560, bottom + 54,
           f"A dot for each of nine countries with a line for its range. {first['name']} is highest with {first['mean']:,} people, {last['name']} is lowest with {last['mean']:,}.",
           parts,
           f"New people of your own age you talk to between 15 and 60, with 94% intervals. {first['name']} leads with about {round(first['mean'], -2):,}. {last['name']} is far below the rest with about {round(last['mean'], -2):,}.")


def guess():
    a, b, low, high = (DATA["guess"][key] for key in ("alpha", "beta", "low", "high"))
    norm = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b))
    density = lambda p: norm * p ** (a - 1) * (1 - p) ** (b - 1)
    left, right, base, top = 30, 530, 236, 34
    peak = density((a - 1) / (a + b - 2))
    x = lambda p: left + (right - left) * p
    y = lambda p: base - (base - top) * density(p) / peak
    grid = [i / 200 for i in range(201)]
    curve = " ".join(f"{x(p):.1f},{y(p):.1f}" for p in grid)
    inside = [p for p in grid if low <= p <= high]
    area = f"{x(low):.1f},{base} " + " ".join(f"{x(p):.1f},{y(p):.1f}" for p in inside) + f" {x(high):.1f},{base}"
    parts = [
        f'<polygon class="tint" points="{area}"/>',
        f'<polyline class="line" points="{curve}"/>',
        f'<line class="thin" x1="{left}" y1="{base}" x2="{right}" y2="{base}"/>',
    ]
    for bound in (low, high):
        parts.append(f'<line class="dash" x1="{x(bound):.1f}" y1="{top - 8}" x2="{x(bound):.1f}" y2="{base}"/>')
    for tick in (0, low, high, 1):
        parts.append(f'<text class="quiet" x="{x(tick):.1f}" y="{base + 20}" text-anchor="middle">{tick:g}</text>')
    parts.append(f'<text x="{x((low + high) / 2):.1f}" y="{base - 62}" text-anchor="middle">90% of my guess</text>')
    parts.append(f'<text class="quiet" x="{(left + right) / 2}" y="{base + 46}" text-anchor="middle">chance that the two recognize each other</text>')
    figure("guess", 560, base + 56,
           f"A curve of plausible values between 0 and 1 with dashed lines at {low:g} and {high:g}. The area between them is filled.",
           parts, "The guess as a curve. 90% of it lies between the two dashed lines.")


def partners():
    rows = DATA["partners"]
    left, right, top, base, lowest = 56, 540, 30, 270, 0.6
    width = (right - left) / len(rows)
    x = lambda i: left + width * (i + 0.5)
    y = lambda share: base - (base - top) * (share - lowest) / (1 - lowest)
    pct = lambda share: f"{share:.0%}"
    parts = []
    for tick in (0.6, 0.7, 0.8, 0.9, 1.0):
        parts.append(f'<line class="thin" x1="{left}" y1="{y(tick):.1f}" x2="{right}" y2="{y(tick):.1f}"/>')
        parts.append(f'<text class="quiet" x="{left - 8}" y="{y(tick) + 4:.1f}" text-anchor="end">{pct(tick)}</text>')
    line = lambda key: " ".join(f"{x(i):.1f},{y(row[key]):.1f}" for i, row in enumerate(rows))
    parts.append(f'<polyline class="dots" points="{line("everyone_same")}"/>')
    parts.append(f'<polyline class="line" points="{line("people_differ")}"/>')
    for i, row in enumerate(rows):
        parts.append(f'<g><title>Ages {row["ages"]}: survey {pct(row["survey"])}, people differ {pct(row["people_differ"])}, everyone the same {pct(row["everyone_same"])}</title>')
        parts.append(f'<rect class="hit" x="{left + width * i:.1f}" y="{top}" width="{width:.1f}" height="{base - top + 26}"/>')
        parts.append(f'<circle class="dot" cx="{x(i):.1f}" cy="{y(row["survey"]):.1f}" r="5.5"/>')
        parts.append(f'<text class="quiet" x="{x(i):.1f}" y="{base + 20}" text-anchor="middle">{row["ages"]}</text></g>')
    first = rows[0]
    parts.append(f'<text x="{x(0) - 12:.1f}" y="{y(first["survey"]) - 9:.1f}" text-anchor="middle">{pct(first["survey"])}</text>')
    parts.append(f'<text x="{x(0) + 12:.1f}" y="{y(first["everyone_same"]) + 17:.1f}" text-anchor="middle">{pct(first["everyone_same"])}</text>')
    parts.append(f'<text class="quiet" x="{(left + right) / 2}" y="{base + 44}" text-anchor="middle">age</text>')
    key = base + 72  # the legend: a dot, a solid line and a dotted line, each with its name
    parts.append(f'<circle class="dot" cx="{left + 6}" cy="{key - 4}" r="5.5"/><text x="{left + 18}" y="{key}">survey</text>')
    parts.append(f'<line class="line" x1="{left + 84}" y1="{key - 4}" x2="{left + 112}" y2="{key - 4}"/><text x="{left + 120}" y="{key}">people differ</text>')
    parts.append(f'<line class="dots" x1="{left + 226}" y1="{key - 4}" x2="{left + 254}" y2="{key - 4}"/><text x="{left + 262}" y="{key}">everyone meets the same number</text>')
    last = rows[-1]
    figure("partners", 560, key + 14,
           f"Shares in the survey rise from {pct(first['survey'])} at ages {first['ages']} to more than {math.floor(last['survey'] * 100)}% at ages {last['ages']}. The solid model line follows them closely. The dotted line starts too low at {pct(first['everyone_same'])}.",
           parts,
           "Share of people who ever had a partner, by age. The dots are the survey. The solid line lets people differ in how many others they meet. The dotted line gives everyone the same number.")


def ages():
    rows = DATA["bands"]
    left, right, top, base, most = 56, 540, 30, 250, 0.8
    width = (right - left) / len(rows)
    x = lambda i: left + width * (i + 0.5)
    y = lambda rate: base - (base - top) * rate / most
    parts = [f'<rect class="tint" x="{left + width * 3:.1f}" y="{top}" width="{width * 9.2:.1f}" height="{base - top}"/>',
             f'<text x="{left + width * 7.6:.1f}" y="{top + 16}" text-anchor="middle">the years I count, 15 to 60</text>']
    for tick in (0, 0.2, 0.4, 0.6, 0.8):
        parts.append(f'<line class="thin" x1="{left}" y1="{y(tick):.1f}" x2="{right}" y2="{y(tick):.1f}"/>')
        parts.append(f'<text class="quiet" x="{left - 8}" y="{y(tick) + 4:.1f}" text-anchor="end">{tick:g}</text>')
    for i, row in enumerate(rows):
        parts.append(f'<g><title>Ages {row["ages"]}: {row["mean"]:.2f} new people a day, range {row["low"]:.2f} to {row["high"]:.2f}</title>')
        parts.append(f'<rect class="hit" x="{left + width * i:.1f}" y="{top}" width="{width:.1f}" height="{base - top + 26}"/>')
        parts.append(f'<line class="line" x1="{x(i):.1f}" y1="{y(row["low"]):.1f}" x2="{x(i):.1f}" y2="{y(row["high"]):.1f}"/>')
        parts.append(f'<circle class="dot" cx="{x(i):.1f}" cy="{y(row["mean"]):.1f}" r="5"/>')
        if i % 2 == 0:  # every second band carries its starting age
            parts.append(f'<text class="quiet" x="{x(i):.1f}" y="{base + 20}" text-anchor="middle">{5 * i}</text>')
        parts.append("</g>")
    peak = max(range(len(rows)), key=lambda i: rows[i]["mean"])
    parts.append(f'<text x="{x(peak) + 12:.1f}" y="{y(rows[peak]["mean"]) - 12:.1f}">{rows[peak]["mean"]:.2f} a day</text>')
    parts.append(f'<text class="quiet" x="{(left + right) / 2}" y="{base + 44}" text-anchor="middle">your age</text>')
    figure("ages", 560, base + 56,
           f"A dot for each 5 year age band with a line for its range. The rate is highest between 20 and 29 with {rows[peak]['mean']:.2f} new people a day and falls with age.",
           parts,
           "New people of your own age you talk to per day, by age, in a typical country. The line is the 94% interval.")


if __name__ == "__main__":
    ages()
    countries()
    guess()
    partners()
    # The check: the numbers the post states in its text are the ones in the data file.
    by_name = {row["name"]: row["mean"] for row in DATA["countries"]}
    youngest = DATA["partners"][0]
    assert by_name["Italy"] == 9626 and by_name["Germany"] == 1770, by_name
    assert (round(youngest["survey"], 2), round(youngest["people_differ"], 2), round(youngest["everyone_same"], 2)) == (0.81, 0.78, 0.68), youngest
    print("wrote 4 charts")
