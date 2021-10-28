from requests import get


def get_user_repos(token, headers={}, etag=None):
    """
        Gets public repository information.
        returns None if user repository information hasn't changed based on the etag
        returns a list of dict if user repository information has been updated
    """
    token = "token "+ token
    headers["Authorization"] = token
    headers["If-None-Match"] = etag
    params = {
        "sort": "pushed",
        "per_page": 100,
    }
    repos_info = {"etag": etag, "repos": []}
    result = get("https://api.github.com/user/repos", headers=headers, params=params)
    if result.status_code == 304:
        return repos_info
    else:
        for repo in result.json():
            repos_info["repos"].append(repo)
        repos_info["etag"] = result.headers.get("etag")
    return repos_info
