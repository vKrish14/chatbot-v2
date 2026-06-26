import asyncio
from backend.app.services.improver import prompt_improver

async def main():
    print("Testing improver...")
    res = await prompt_improver.improve_prompt("Hello world")
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
