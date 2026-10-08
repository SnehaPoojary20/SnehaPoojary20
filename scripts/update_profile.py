#!/usr/bin/env python3
"""Refresh live numbers for the profile README.

Pulls GitHub contributions, LeetCode stats and Hashnode posts from their public
APIs, merges them over data/stats.json (the Apify snapshot is the fallback when
an API is unreachable), then regenerates assets/stats.svg and the blog-post
block inside README.md.

Usage:  GITHUB_TOKEN=... python scripts/update_profile.py
"""
import datetime as dt
import html
import json
import os
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "stats.json"
README = ROOT / "README.md"
SVG_OUT = ROOT / "assets" / "stats.svg"

GH_USER = "SnehaPoojary20"
LC_USER = "SnehaPoojary__"
HN_USER = "snehapoojary"


def post_json(url, payload, headers=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "profile-updater", **(headers or {})},
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.load(resp)


# ---------- fetchers (each returns a dict of fields to merge, or {} on failure) ----------

def fetch_github(token):
    if not token:
        return {}
    hdr = {"Authorization": f"Bearer {token}"}
    gql = "https://api.github.com/graphql"
    try:
        first = post_json(gql, {"query": 'query{user(login:"%s"){createdAt followers{totalCount} following{totalCount}}}' % GH_USER}, hdr)
        user = first["data"]["user"]
        created = dt.datetime.fromisoformat(user["createdAt"].replace("Z", "+00:00"))
        now = dt.datetime.now(dt.timezone.utc)
        total = 0
        year = created.year
        while year <= now.year:  # contributionsCollection covers max 1 year per query
            start = max(created, dt.datetime(year, 1, 1, tzinfo=dt.timezone.utc))
            end = min(now, dt.datetime(year, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc))
            q = ('query{user(login:"%s"){contributionsCollection(from:"%s",to:"%s")'
                 '{contributionCalendar{totalContributions}}}}') % (GH_USER, start.isoformat(), end.isoformat())
            r = post_json(gql, {"query": q}, hdr)
            total += r["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
            year += 1
        return {"contributions": total, "followers": user["followers"]["totalCount"], "following": user["following"]["totalCount"]}
    except Exception as e:  # noqa: BLE001
        print("github fetch failed:", e)
        return {}


def fetch_leetcode():
    q = """query($u:String!){matchedUser(username:$u){
      submitStatsGlobal{acSubmissionNum{difficulty count}}
      languageProblemCount{languageName problemsSolved}
      tagProblemCounts{fundamental{tagName problemsSolved} intermediate{tagName problemsSolved} advanced{tagName problemsSolved}}}}"""
    try:
        r = post_json("https://leetcode.com/graphql", {"query": q, "variables": {"u": LC_USER}},
                      {"Referer": "https://leetcode.com"})
        m = r["data"]["matchedUser"]
        ac = {x["difficulty"]: x["count"] for x in m["submitStatsGlobal"]["acSubmissionNum"]}
        tags = [t for grp in m["tagProblemCounts"].values() for t in grp]
        tags.sort(key=lambda t: -t["problemsSolved"])
        # keep tags that read well on a recruiter-facing card
        skip = {"Database"}
        topics = [{"name": t["tagName"], "solved": t["problemsSolved"]} for t in tags if t["tagName"] not in skip][:7]
        langs = sorted(m["languageProblemCount"], key=lambda l: -l["problemsSolved"])
        return {
            "solved": ac["All"], "easy": ac["Easy"], "medium": ac["Medium"], "hard": ac["Hard"],
            "languages": [{"name": l["languageName"], "solved": l["problemsSolved"]} for l in langs[:3]],
            "topics": topics,
        }
    except Exception as e:  # noqa: BLE001
        print("leetcode fetch failed:", e)
        return {}


def fetch_hashnode():
    q = """query($u:String!){user(username:$u){posts(page:1,pageSize:5){nodes{title url publishedAt readTimeInMinutes}}}}"""
    try:
        r = post_json("https://gql.hashnode.com", {"query": q, "variables": {"u": HN_USER}})
        nodes = r["data"]["user"]["posts"]["nodes"]
        return {"posts": [{"title": n["title"], "url": n["url"].split("?")[0],
                           "date": n["publishedAt"][:10], "minutes": n["readTimeInMinutes"]} for n in nodes]}
    except Exception as e:  # noqa: BLE001
        print("hashnode fetch failed:", e)
        return {}


# ---------- rendering ----------

def fmt_date(iso):
    d = dt.date.fromisoformat(iso)
    return d.strftime("%b %d, %Y").replace(" 0", " ")


def render_svg(s):
    gh, lc, hn = s["github"], s["leetcode"], s["hashnode"]
    contrib = f'{gh["contributions"]:,}' if gh.get("contributions") is not None else "-"
    tiles = [
        (f'{lc["solved"]}', "LeetCode solved"),
        (contrib, "GitHub contributions"),
        (f'{len(hn["posts"])}', "Technical articles"),
        ("3", "Live deployments"),
    ]
    tile_svg = ""
    for i, (num, label) in enumerate(tiles):
        x = 32 + i * 214
        tile_svg += (
            f'<g transform="translate({x} 28)"><rect class="tile" width="198" height="96" rx="12"/>'
            f'<text class="num" x="20" y="52">{html.escape(num)}</text>'
            f'<text class="lbl" x="20" y="78">{html.escape(label)}</text></g>'
        )

    # difficulty bar
    total = max(lc["easy"] + lc["medium"] + lc["hard"], 1)
    bw = 380
    ew, mw = bw * lc["easy"] / total, bw * lc["medium"] / total
    hw = bw - ew - mw
    diff = (
        '<text class="h" x="32" y="170">Problem difficulty</text>'
        f'<g transform="translate(32 186)"><rect x="0" width="{ew:.1f}" height="14" rx="3" fill="#34d399"/>'
        f'<rect x="{ew + 3:.1f}" width="{max(mw - 3, 0):.1f}" height="14" rx="3" fill="#fbbf24"/>'
        f'<rect x="{ew + mw + 3:.1f}" width="{max(hw - 3, 0):.1f}" height="14" rx="3" fill="#f87171"/></g>'
        f'<text class="sm" x="32" y="228">Easy {lc["easy"]}  ·  Medium {lc["medium"]}  ·  Hard {lc["hard"]}</text>'
        f'<text class="sm" x="32" y="252">{lc["acceptance"]}% acceptance across {lc["submissions"]} submissions</text>'
    )
    if lc.get("languages"):
        langs = "  ·  ".join(f'{l["name"]} {l["solved"]}' for l in lc["languages"])
        diff += f'<text class="sm" x="32" y="276">{html.escape(langs)}</text>'

    # topics
    topics = lc["topics"][:6]
    top = max(t["solved"] for t in topics)
    topic_svg = '<text class="h" x="480" y="170">Strongest topics</text>'
    for i, t in enumerate(topics):
        y = 190 + i * 24
        w = 150 * t["solved"] / top
        topic_svg += (
            f'<text class="sm" x="480" y="{y + 11}">{html.escape(t["name"])}</text>'
            f'<rect x="640" y="{y}" width="{w:.1f}" height="12" rx="3" fill="url(#g)"/>'
            f'<text class="sm" x="{640 + w + 8:.1f}" y="{y + 11}">{t["solved"]}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 340" width="900" height="340" role="img" aria-label="Coding stats">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#7dd3fc"/><stop offset="1" stop-color="#a78bfa"/></linearGradient></defs>
<style>
  :root {{ --bg:#0f172a; --tile:#1e293b; --fg:#f8fafc; --mute:#94a3b8; --line:#334155; }}
  @media (prefers-color-scheme: light) {{ :root {{ --bg:#ffffff; --tile:#f1f5f9; --fg:#0f172a; --mute:#475569; --line:#e2e8f0; }} }}
  text {{ font-family: -apple-system,"Segoe UI",Inter,Helvetica,Arial,sans-serif; fill: var(--fg); }}
  .card {{ fill: var(--bg); stroke: var(--line); }}
  .tile {{ fill: var(--tile); }}
  .num {{ font-size: 36px; font-weight: 800; }}
  .lbl {{ font-size: 13px; fill: var(--mute); }}
  .h {{ font-size: 14px; font-weight: 700; letter-spacing: .5px; }}
  .sm {{ font-size: 13px; fill: var(--mute); }}
</style>
<rect class="card" x="0.5" y="0.5" width="899" height="339" rx="16"/>
{tile_svg}
{diff}
{topic_svg}
<text class="sm" x="868" y="326" text-anchor="end" style="font-size:11px">Updated {fmt_date(s["updated"])} · auto-refreshed daily by GitHub Actions</text>
</svg>
'''


def render_posts(posts):
    lines = [f'- [{p["title"]}]({p["url"]}) · {fmt_date(p["date"])} · {p["minutes"]} min read' for p in posts]
    return "\n".join(lines)


def main():
    stats = json.loads(DATA.read_text())
    stats["github"].update(fetch_github(os.environ.get("GITHUB_TOKEN")))
    stats["leetcode"].update(fetch_leetcode())
    stats["hashnode"].update(fetch_hashnode())
    stats["updated"] = dt.date.today().isoformat()
    DATA.write_text(json.dumps(stats, indent=2) + "\n")

    SVG_OUT.write_text(render_svg(stats))

    text = README.read_text()
    block = f'<!--POSTS:START-->\n{render_posts(stats["hashnode"]["posts"])}\n<!--POSTS:END-->'
    text = re.sub(r"<!--POSTS:START-->.*?<!--POSTS:END-->", lambda _: block, text, flags=re.S)
    README.write_text(text)
    print("profile refreshed")


if __name__ == "__main__":
    main()
