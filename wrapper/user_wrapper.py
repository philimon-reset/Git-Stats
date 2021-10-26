from requests import get


def get_user(token, etag=None, headers={}):
    """
        Gets public user information.
        returns None if user information hasn't changed based on the etag
        returns a dict if user information has been updated
    """
    token = "token "+ token
    headers["Authorization"] = token
    headers["If-None-Match"] = etag

    result = get("https://api.github.com/user", headers=headers)
    if result.status_code == 304:
        return None
    else:
        return result
