import requests
import pandas as pd
import os

# Ensure dataset directory exists
os.makedirs("dataset", exist_ok=True)

# GitHub API settings
GITHUB_API_URL = "https://api.github.com/search/repositories"
HEADERS = {"Accept": "application/vnd.github.v3+json"}

def fetch_repositories(query="language:python stars:>50", per_page=10):
    """
    Fetches the top Python repositories from GitHub API based on stars.

    Args:
        query (str): Search query for GitHub API (default: Python projects with >50 stars).
        per_page (int): Number of repositories to fetch (default: 10).

    Returns:
        pd.DataFrame: Dataframe containing repository names, URLs, and stars.
    """
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": per_page}
    response = requests.get(GITHUB_API_URL, headers=HEADERS, params=params)

    if response.status_code == 200:
        repos = response.json()["items"]
        data = [{"name": repo["name"], "url": repo["html_url"], "stars": repo["stargazers_count"]} for repo in repos]
        return pd.DataFrame(data)
    else:
        print("Error fetching repositories:", response.status_code, response.text)
        return pd.DataFrame()

# Fetch and save repositories
df_repos = fetch_repositories()
if not df_repos.empty:
    df_repos.to_csv("dataset/github_repos.csv", index=False)
    print("GitHub repository data saved in dataset/github_repos.csv!")
else:
    print("No data fetched. Check API response or query parameters.")
