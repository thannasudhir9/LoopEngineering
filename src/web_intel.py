"""
Web Intelligence — fetch trending repos, posts, articles from public APIs.
GitHub, Reddit, Hacker News, Dev.to. No auth required for public endpoints.
"""
import asyncio
import httpx

_UA = "LoopEngineering/1.0 (AI Task Dashboard)"
_HEADERS = {"User-Agent": _UA, "Accept": "application/json"}


async def search_github(query: str, per_page: int = 10) -> list[dict]:
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": per_page}
    async with httpx.AsyncClient(timeout=15, headers={**_HEADERS, "Accept": "application/vnd.github.v3+json"}) as c:
        r = await c.get(url, params=params)
    if r.status_code != 200:
        return []
    return [{
        "source": "github",
        "title": i["full_name"],
        "desc": i.get("description") or "",
        "url": i["html_url"],
        "stars": i["stargazers_count"],
        "forks": i["forks_count"],
        "language": i.get("language") or "",
        "topics": i.get("topics", []),
        "updated": i["updated_at"],
        "owner_avatar": i["owner"]["avatar_url"],
    } for i in r.json().get("items", [])]


async def search_reddit(query: str, subreddits: list[str] | None = None, limit: int = 10) -> list[dict]:
    subs = "+".join(subreddits or ["salesforce", "mulesoft", "apexcode", "devops", "programming"])
    url = f"https://www.reddit.com/r/{subs}/search.json"
    params = {"q": query, "limit": limit, "sort": "relevance", "t": "month", "restrict_sr": "on"}
    async with httpx.AsyncClient(timeout=15, headers={**_HEADERS, "User-Agent": _UA}, follow_redirects=True) as c:
        r = await c.get(url, params=params)
    if r.status_code != 200:
        return []
    return [{
        "source": "reddit",
        "title": p["data"]["title"],
        "desc": (p["data"].get("selftext") or "")[:300],
        "url": "https://reddit.com" + p["data"]["permalink"],
        "score": p["data"]["score"],
        "comments": p["data"]["num_comments"],
        "subreddit": p["data"]["subreddit"],
        "author": p["data"]["author"],
    } for p in r.json().get("data", {}).get("children", [])]


async def search_hackernews(query: str, limit: int = 10) -> list[dict]:
    url = "https://hn.algolia.com/api/v1/search"
    params = {"query": query, "tags": "story", "hitsPerPage": limit}
    async with httpx.AsyncClient(timeout=15, headers=_HEADERS) as c:
        r = await c.get(url, params=params)
    if r.status_code != 200:
        return []
    return [{
        "source": "hackernews",
        "title": h.get("title", ""),
        "desc": "",
        "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
        "score": h.get("points", 0),
        "comments": h.get("num_comments", 0),
        "author": h.get("author", ""),
        "created": h.get("created_at", ""),
    } for h in r.json().get("hits", []) if h.get("title")]


async def search_devto(query: str, limit: int = 10) -> list[dict]:
    url = "https://dev.to/api/articles"
    tag = query.lower().replace(" ", "").replace("-", "")[:20]
    params = {"per_page": limit, "tag": tag}
    async with httpx.AsyncClient(timeout=15, headers=_HEADERS) as c:
        r = await c.get(url, params=params)
    if r.status_code != 200:
        return []
    return [{
        "source": "devto",
        "title": a["title"],
        "desc": a.get("description", ""),
        "url": a["url"],
        "score": a.get("positive_reactions_count", 0),
        "comments": a.get("comments_count", 0),
        "author": a.get("user", {}).get("name", ""),
        "tags": a.get("tag_list", []),
    } for a in r.json() if isinstance(a, dict)]


async def multi_search(query: str, sources: list[str], limit: int = 8) -> dict:
    """Search requested sources in parallel."""
    jobs: dict[str, object] = {}
    if "github" in sources:
        jobs["github"] = search_github(query, per_page=limit)
    if "reddit" in sources:
        jobs["reddit"] = search_reddit(query, limit=limit)
    if "hackernews" in sources:
        jobs["hackernews"] = search_hackernews(query, limit=limit)
    if "devto" in sources:
        jobs["devto"] = search_devto(query, limit=limit)
    results = await asyncio.gather(*jobs.values(), return_exceptions=True)
    return {k: (v if not isinstance(v, Exception) else []) for k, v in zip(jobs.keys(), results)}
