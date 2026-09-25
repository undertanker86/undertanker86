"""Generate GitHub-style repo pin cards (Tokyo Night theme) as SVG files."""
import json
import os
import textwrap
import urllib.request
from xml.sax.saxutils import escape

USER = "undertanker86"
REPOS = [
    "data-pipeline-with-dbt-dagster",
    "Vietnam-Air-Quality-Data-Pipeline",
    "Facial--Expression-Recognition-MLOps",
    "End-to-end-fraud-detection-lab",
    "Project-Visual-Question-Answering",
]
# Optional: override the title or description shown on a card
TITLE_OVERRIDE = {
    "Facial--Expression-Recognition-MLOps": "CV-MLOps-Pipeline",
}
DESC_OVERRIDE = {}

OUT_DIR = "assets/pins"
LANG_COLORS = {
    "Python": "#3572A5", "Jupyter Notebook": "#DA5B0B", "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6", "Shell": "#89e051", "HTML": "#e34c26",
    "Dockerfile": "#384d54", "Go": "#00ADD8", "SQL": "#e38c00", "HCL": "#844FBA",
}
BG, TITLE, TEXT, ICON = "#1a1b27", "#70a5fd", "#38bdae", "#bf91f3"

REPO_ICON = ("M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5"
             "a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9z"
             "m10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087"
             "a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z")
STAR_ICON = ("M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192"
             "a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01"
             ".416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z")
FORK_ICON = ("M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 0v.878A2.25 2.25 0 005.75"
             " 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5a2.25 2.25 0 002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878"
             "a.75.75 0 01-.75.75h-4.5A.75.75 0 015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm3-8.75"
             "a.75.75 0 100-1.5.75.75 0 000 1.5z")


def fetch(repo):
    req = urllib.request.Request(f"https://api.github.com/repos/{USER}/{repo}")
    token = os.getenv("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def card(repo, data):
    title = escape(TITLE_OVERRIDE.get(repo, data["name"]))
    desc = DESC_OVERRIDE.get(repo, data.get("description") or "No description provided.")
    lines = textwrap.wrap(desc, 56)[:2]
    if len(textwrap.wrap(desc, 56)) > 2:
        lines[1] = lines[1][:53].rstrip() + "..."
    desc_svg = "".join(
        f'<tspan x="25" dy="{0 if i == 0 else 18}">{escape(l)}</tspan>' for i, l in enumerate(lines)
    )
    lang = data.get("language") or "Other"
    color = LANG_COLORS.get(lang, "#858585")
    stars, forks = data.get("stargazers_count", 0), data.get("forks_count", 0)
    lang_w = 30 + len(lang) * 7
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="120" viewBox="0 0 400 120">
  <style>
    .t {{ font: 600 16px 'Segoe UI', Ubuntu, sans-serif; fill: {TITLE}; }}
    .d {{ font: 400 13px 'Segoe UI', Ubuntu, sans-serif; fill: {TEXT}; }}
    .g {{ font: 400 12px 'Segoe UI', Ubuntu, sans-serif; fill: {TEXT}; }}
  </style>
  <rect x="0.5" y="0.5" rx="6" width="399" height="119" fill="{BG}"/>
  <path transform="translate(25,19)" fill="{ICON}" d="{REPO_ICON}"/>
  <text x="48" y="32" class="t">{title}</text>
  <text x="25" y="58" class="d">{desc_svg}</text>
  <g transform="translate(25,100)">
    <circle cx="6" cy="-4" r="6" fill="{color}"/>
    <text x="17" y="0" class="g">{escape(lang)}</text>
    <path transform="translate({lang_w},-15)" fill="{ICON}" d="{STAR_ICON}"/>
    <text x="{lang_w + 22}" y="0" class="g">{stars}</text>
    <path transform="translate({lang_w + 55},-15)" fill="{ICON}" d="{FORK_ICON}"/>
    <text x="{lang_w + 77}" y="0" class="g">{forks}</text>
  </g>
</svg>
'''


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for repo in REPOS:
        data = fetch(repo)
        with open(os.path.join(OUT_DIR, f"{repo}.svg"), "w", encoding="utf-8") as f:
            f.write(card(repo, data))
        print("generated", repo)


if __name__ == "__main__":
    main()
