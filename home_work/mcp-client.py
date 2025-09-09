import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(
        command="cmd",
        args=["/c", "python", "mcp_server.py"]
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Available tools:", await session.list_tools())
            res = await session.call_tool("search_blog", {"query": "Python", "display": 3})
            print("Result:", res.content)

if __name__ == "__main__":
    asyncio.run(main())