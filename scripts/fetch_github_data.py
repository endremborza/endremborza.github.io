import json
import os

import requests

GITHUB_USERNAME = "endremborza"  # Replace with your GitHub username
APP_LIST_PATH = "static/notes/applets.md"
OUTPUT_PATH = "src/lib/data/github-repos.json"


def fetch_github_data():
    # Read desired repositories from applets.md
    desired_repos = set()
    if os.path.exists(APP_LIST_PATH):
        with open(APP_LIST_PATH, "r") as f:
            for line in f:
                repo_name = line.strip()
                if repo_name and not repo_name.startswith("#"):
                    desired_repos.add(
                        repo_name.lower()
                    )  # Store in lowercase for case-insensitive matching
    else:
        print(
            f"Warning: {APP_LIST_PATH} not found. No specific repositories to filter."
        )
        # If applets.md is not found, we will try to fetch all public repos for the user
        # and not filter by a specific list. This might not be the desired behavior,
        # but it prevents an empty output if applets.md is missing.
    print(desired_repos)
    return

    # Fetch all public repositories for the user
    all_user_repos = []
    page = 1
    while True:
        print(f"Fetching public repositories for {GITHUB_USERNAME}, page {page}...")
        url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100&page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            current_page_repos = response.json()
            if not current_page_repos:
                break  # No more pages
            all_user_repos.extend(current_page_repos)
            page += 1
        else:
            print(
                f"Error fetching all repositories for {GITHUB_USERNAME}: {response.status_code}"
            )
            break

    github_data = []
    for repo_data in all_user_repos:
        repo_name_lower = repo_data["name"].lower()
        if not desired_repos or repo_name_lower in desired_repos:
            print(f"Processing repository: {repo_data['name']}")
            github_data.append(
                {
                    "name": repo_data["name"],
                    "description": repo_data["description"],
                    "html_url": repo_data["html_url"],
                    "stargazers_count": repo_data["stargazers_count"],
                    "language": repo_data["language"],
                    "updated_at": repo_data["updated_at"],
                }
            )

    # Ensure output directory exists
    output_dir = os.path.dirname(OUTPUT_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(github_data, f, indent=2)
    print(f"Successfully fetched GitHub data and saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    fetch_github_data()

