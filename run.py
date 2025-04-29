from agent import root_agent
import asyncio

async def main():
    user_input = input("Ask about weather or time in a city: ")
    try:
        response = await root_agent.process(user_input) # Trying 'process'
        print(response)
    except AttributeError as e:
        print(f"Error: {e}")
        print("It seems 'process' is also not a direct attribute.")
        print("Please consult the google-adk library documentation for the correct way to interact with the Agent object.")

if __name__ == "__main__":
    asyncio.run(main())