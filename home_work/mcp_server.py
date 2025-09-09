# server.py
import os
import requests
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context

mcp = FastMCP("naver-agent")

@mcp.tool()
def search_blog(query: str, display: int = 5, start: int = 1, sort: str = "sim") -> dict:
    res = requests.get(
        "https://openapi.naver.com/v1/search/blog.json",
        params={"query": query, "display": display, "start": start, "sort": sort},
        headers={
            "X-Naver-Client-Id": "WWQjcNZM_nd8F1QhxO70",
            "X-Naver-Client-Secret": "aX7U5x3ynt",
        },
    )
    res.raise_for_status()
    return res.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")