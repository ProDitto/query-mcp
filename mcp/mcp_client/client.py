from fastmcp import Client
from google import genai
import asyncio
from dotenv import load_dotenv
import sys

load_dotenv()

try:
    mcp_client = Client("./mcp_server/server.py")
except Exception as e:
    print("Handle me : ", e)

gemini_client = genai.Client()

async def chat_loop():
    async with mcp_client:
        chat_history = []  # List to keep track of chat history

        while True:
            # Get user input
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Exiting chat...")
                break
            
            # Add user input to chat history
            chat_history.append(f"You: {user_input}")
            
            # Combine all chat history into one string (can also format with newlines)
            chat_context = "\n".join(chat_history)

            # Send the chat history as context to the model
            response = await gemini_client.aio.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=chat_context,
                config=genai.types.GenerateContentConfig(
                    temperature=0.7,  # Adjust temperature as needed
                    tools=[mcp_client.session],  # Pass the FastMCP client session
                ),
            )
            
            # Print model's response
            print(f"Gemini: {response.text}")
            
            # Add the model's response to chat history
            chat_history.append(f"Gemini: {response.text}")

if __name__ == "__main__":
    # asyncio.run(chat_loop())
    print("client")
