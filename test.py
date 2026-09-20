import asyncio

from deepagents import create_deep_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from models import model

user_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjA4YjhiOWMwLTc3YjktNDZlOC04OWMzLWQzNmUxMjIzYzllZSIsInJvbGUiOiJBRE1JTiIsImxvZ2luX2hpc3RvcnlfaWQiOiIwMmFlZjExOS01MTQ3LTRhYmEtOWUwNy1kMTAzZjhlYmQ4ZWQiLCJpYXQiOjE3ODg1MzUwMTAsImV4cCI6MTc4ODUzODYxMH0.Wr0iKG2zbzs8qEE6Pe5xCzMl1zR9dsB_RTAo6hnYfQQ"
async def main():
    client = MultiServerMCPClient({
        "docs-langchain": {
            "transport": "http",
            "url": "http://localhost:3001/mcp",
              "headers": {
            "Authorization": f"Bearer {user_jwt}",
        },
        }
    })
    tools = await client.get_tools()

    print(f"\nZellibook Tools: {len(tools)} tool(s)")
    for t in tools:
        print(f"  {t.name}")
        print(f"  {t.description[:90]}")

    ALLOWED = {"GetApiV1Invoice"}
    tools = [t for t in tools if t.name in ALLOWED]
    
    print(f"\nfiltered to: {len(tools)} tool(s)")
    for t in tools:
        print(f"  {t.name}")
    

    agent = create_deep_agent(model=model, tools=tools)

    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": "i need a list of all my invoices"}]
    })
    print(result["messages"][-1].content)


asyncio.run(main())