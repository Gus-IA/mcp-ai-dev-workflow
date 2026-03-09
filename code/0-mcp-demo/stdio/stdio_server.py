import asyncio
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import SamplingMessage, TextContent

mcp = FastMCP(name="0-mcp-intro-weather")


@mcp.tool()
async def get_weather(city: str, ctx: Context) -> int:
    """
    Returns the temperature for a given city (dummy example).
    """
    return 22


@mcp.resource("file://test_json.md")
def get_file() -> str:
    """
    Example resource returning file content.
    """
    return "Content of the file"


@mcp.tool()
async def summarize(text_to_summarize: str, ctx: Context) -> str:
    """
    Uses the model available to the client to summarize text.
    """
    prompt = f"""
Please summarize the following text:

{text_to_summarize}
"""

    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(type="text", text=prompt),
            )
        ],
        max_tokens=4000,
        system_prompt="You are a helpful research assistant.",
    )

    if result.content.type == "text":
        return result.content.text
    else:
        raise ValueError("Sampling failed")


@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    """
    Demonstrates progress reporting.
    """
    await ctx.info("Preparing to add...")
    await ctx.report_progress(20, 100)

    await asyncio.sleep(2)

    await ctx.info("Adding numbers...")
    await ctx.report_progress(80, 100)

    return a + b


@mcp.tool()
async def list_folders_under_roots(ctx: Context):
    """
    Lists folders available from the client roots.
    """
    roots = await ctx.session.list_roots()

    if not roots:
        return {"error": "No client roots available in context."}

    return {"roots": roots}


if __name__ == "__main__":
    # IMPORTANT: never print to stdout in MCP stdio servers
    mcp.run(transport="stdio")
