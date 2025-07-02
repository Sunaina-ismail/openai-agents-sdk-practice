import asyncio

async def delay() -> str:
    print("hello world")
    await asyncio.sleep(4)
    return "hello"

