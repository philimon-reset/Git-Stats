from requests import get


def get_user_repos(token, user_id, headers={}, etag=None):
    """
        Gets public repository information.
        returns None if user repository information hasn't changed based on the etag
        returns a list of dict if user repository information has been updated
    """
    token = "token " + token
    headers["Authorization"] = token
    headers["If-None-Match"] = etag
    params = {
        "sort": "pushed",
        "per_page": 100,
        "visibility": "public"
    }
    repos_info = {"etag": etag, "repos": []}
    result = get(
        "https://api.github.com/user/repos",
        headers=headers,
        params=params)
    if result.status_code == 304:
        return repos_info
    else:
        for repo in result.json():
            repo["owner_id"] = repo["owner"]["id"]
            repo["repo_owner_name"] = repo["owner"]["login"]
            repo["repo_owner_url"] = repo["owner"]["html_url"]
            repo["user_id"] = user_id
            repos_info["repos"].append(repo)
        repos_info["etag"] = result.headers.get("etag")
    return repos_info
