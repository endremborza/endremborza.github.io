"""Collect public profile data from OpenAlex and GitHub.

Outputs a JSON snapshot to data/profiles/snapshot.json with timestamped data
from each source. Run periodically to track career metrics over time.

Usage: python scripts/collect_profiles.py
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "profiles"
SNAPSHOT_PATH = OUTPUT_DIR / "snapshot.json"
HISTORY_PATH = OUTPUT_DIR / "history.json"

OPENALEX_AUTHOR = "https://api.openalex.org/a5042797356"
OPENALEX_WORKS = "https://api.openalex.org/works?filter=author.id:a5042797356&sort=cited_by_count:desc&per_page=50"
GITHUB_USER = "endremborza"


def fetch_json(url: str) -> dict:
    req = Request(url, headers={"User-Agent": "collect-profiles/1.0"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def collect_openalex() -> dict:
    author = fetch_json(OPENALEX_AUTHOR)
    works_resp = fetch_json(OPENALEX_WORKS)

    works = []
    for w in works_resp.get("results", []):
        works.append({
            "title": w.get("title", ""),
            "year": w.get("publication_year"),
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "cited_by_count": w.get("cited_by_count", 0),
            "doi": w.get("doi"),
            "type": w.get("type"),
            "is_oa": w.get("open_access", {}).get("is_oa", False),
        })

    topics = []
    for t in author.get("topics", [])[:10]:
        topics.append({
            "name": t.get("display_name", ""),
            "score": t.get("score", 0),
        })

    return {
        "name": author.get("display_name", ""),
        "orcid": author.get("orcid"),
        "works_count": author.get("works_count", 0),
        "cited_by_count": author.get("cited_by_count", 0),
        "h_index": author.get("summary_stats", {}).get("h_index", 0),
        "i10_index": author.get("summary_stats", {}).get("i10_index", 0),
        "two_year_mean_citedness": author.get("summary_stats", {}).get("2yr_mean_citedness", 0),
        "topics": topics,
        "works": works,
        "affiliations": [
            {
                "institution": a.get("institution", {}).get("display_name", ""),
                "years": a.get("years", []),
            }
            for a in author.get("affiliations", [])[:5]
        ],
    }


def collect_github() -> dict:
    gh_cmd = ["gh", "api"]

    def gh_api(endpoint: str) -> dict | list:
        result = subprocess.run(
            [*gh_cmd, endpoint],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print(f"gh api {endpoint} failed: {result.stderr}", file=sys.stderr)
            return {}
        return json.loads(result.stdout)

    user = gh_api(f"users/{GITHUB_USER}")

    repos_raw = subprocess.run(
        [*gh_cmd, f"users/{GITHUB_USER}/repos", "--paginate"],
        capture_output=True, text=True, timeout=60,
    )
    all_repos = json.loads(repos_raw.stdout) if repos_raw.returncode == 0 else []

    repos = []
    total_stars = 0
    total_forks = 0
    languages: dict[str, int] = {}

    for r in all_repos:
        if r.get("fork"):
            continue
        stars = r.get("stargazers_count", 0)
        forks = r.get("forks_count", 0)
        total_stars += stars
        total_forks += forks
        lang = r.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
        repos.append({
            "name": r["name"],
            "description": r.get("description"),
            "language": lang,
            "stars": stars,
            "forks": forks,
            "updated_at": r.get("updated_at"),
            "topics": r.get("topics", []),
        })

    repos.sort(key=lambda x: x["stars"], reverse=True)

    contrib_query = """{ user(login: "%s") {
        contributionsCollection {
            contributionCalendar { totalContributions }
            totalCommitContributions
            totalPullRequestContributions
            totalIssueContributions
            totalPullRequestReviewContributions
        }
    }}""" % GITHUB_USER

    contrib_result = subprocess.run(
        [*gh_cmd, "graphql", "-f", f"query={contrib_query}"],
        capture_output=True, text=True, timeout=30,
    )
    contributions = {}
    if contrib_result.returncode == 0:
        cdata = json.loads(contrib_result.stdout)
        cc = cdata.get("data", {}).get("user", {}).get("contributionsCollection", {})
        contributions = {
            "total_last_year": cc.get("contributionCalendar", {}).get("totalContributions", 0),
            "commits": cc.get("totalCommitContributions", 0),
            "pull_requests": cc.get("totalPullRequestContributions", 0),
            "issues": cc.get("totalIssueContributions", 0),
            "reviews": cc.get("totalPullRequestReviewContributions", 0),
        }

    return {
        "login": user.get("login", GITHUB_USER),
        "name": user.get("name"),
        "bio": user.get("bio"),
        "location": user.get("location"),
        "company": user.get("company"),
        "blog": user.get("blog"),
        "hireable": user.get("hireable"),
        "followers": user.get("followers", 0),
        "following": user.get("following", 0),
        "public_repos": user.get("public_repos", 0),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "languages": dict(sorted(languages.items(), key=lambda x: -x[1])),
        "top_repos": repos[:15],
        "contributions": contributions,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()

    print("Collecting OpenAlex data...")
    openalex = collect_openalex()

    print("Collecting GitHub data...")
    github = collect_github()

    snapshot = {
        "collected_at": now,
        "openalex": openalex,
        "github": github,
    }

    SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2))
    print(f"Snapshot written to {SNAPSHOT_PATH}")

    history: list[dict] = []
    if HISTORY_PATH.exists():
        history = json.loads(HISTORY_PATH.read_text())

    history.append({
        "date": now,
        "openalex_citations": openalex["cited_by_count"],
        "openalex_h_index": openalex["h_index"],
        "openalex_works": openalex["works_count"],
        "github_stars": github["total_stars"],
        "github_followers": github["followers"],
        "github_contributions_last_year": github.get("contributions", {}).get("total_last_year", 0),
        "github_public_repos": github["public_repos"],
    })

    HISTORY_PATH.write_text(json.dumps(history, indent=2))
    print(f"History appended to {HISTORY_PATH}")

    print("\n--- Summary ---")
    print(f"OpenAlex: {openalex['works_count']} works, {openalex['cited_by_count']} citations, h-index {openalex['h_index']}")
    print(f"GitHub: {github['public_repos']} repos, {github['total_stars']} stars, {github['followers']} followers")
    contribs = github.get("contributions", {})
    if contribs:
        print(f"  Last year: {contribs.get('total_last_year', '?')} contributions ({contribs.get('commits', '?')} commits, {contribs.get('pull_requests', '?')} PRs)")

    missing_desc = [r["name"] for r in github["top_repos"] if not r.get("description")]
    if missing_desc:
        print(f"\n  Repos missing descriptions: {', '.join(missing_desc[:10])}")

    if not github.get("bio"):
        print("  GitHub bio is empty")
    if not github.get("hireable"):
        print("  GitHub hireable is not set")
    if not github.get("blog"):
        print("  GitHub blog URL is empty")


if __name__ == "__main__":
    main()
