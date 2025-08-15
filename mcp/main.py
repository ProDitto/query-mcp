import asyncio
from mcp_client.client import chat_loop

if __name__=="__main__":
    print("main")
    asyncio.run(chat_loop())
