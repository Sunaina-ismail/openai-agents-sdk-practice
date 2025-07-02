import asyncio
import inspect

async def func_a():
    await asyncio.sleep(5)
    return "hello world"

async def func_b():
    output=func_a()
    if inspect.isawaitable(output):
        return await output

async def main():
    final_output=await func_b()
    print(final_output)

asyncio.run(main())   


