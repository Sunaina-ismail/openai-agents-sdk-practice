import asyncio

async def func_a():
    print("func a is started")
    await asyncio.sleep(5)
    print("func a is ended")
    return "result of func a"

async def func_b():
    print("func b is started")
    await asyncio.sleep(10)
    print("func b is ended")
    return "result of func b"

async def main():
    result_a, result_b = await asyncio.gather(
        func_a(),
        func_b(),
    )
    print(result_a)
    print(result_b)

asyncio.run(main())

"""
func a is started
func a is ended
func b is started
func b is ended
result of func a
result of func b
"""


"""
func a is started
func b is started
func a is ended
func b is ended
result of func a
result of func b
"""












"""
You're using time.sleep(), which is a blocking function. This pauses the entire thread, including the event loop — so your async coroutines do not run concurrently.
"""