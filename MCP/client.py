from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent   # deprecation warning fix bhi kar diya
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def main():
    client = MultiServerMCPClient({
        "math": {
            "command": "python",
            "args": ["MCP/mathserver.py"],
            "transport": "stdio"
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable-http"
        }
    })

    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

    tools = await client.get_tools()

    model = init_chat_model("google_genai:gemini-2.5-flash")

    agent = create_agent(
        tools=tools,
        model=model,
    )

    math_response = await agent.ainvoke({"messages": [{"role": "user", "content": "What is 2+2?"}]})
    print(math_response["messages"][-1].content)

    weather_response = await agent.ainvoke({"messages": [{"role": "user", "content": "What is the weather in Boston?"}]})
    print(weather_response["messages"][-1].content)

asyncio.run(main())