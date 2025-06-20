import asyncio
import random

async def dost_ka_kaam(naam, kaam):
    random_time=random.randint(0,10)
    print(f"{naam} gaya {kaam} lene... {random_time}")
    await asyncio.sleep(random_time)  # Samjho 2 min lag rahe hain
    print(f"{naam} wapas aa gaya {kaam} le kar.")
    return f"{naam} ne {kaam} le aaya."

async def main():
    tasks = [
        asyncio.create_task(dost_ka_kaam("Ahmed", "doodh")),
        asyncio.create_task(dost_ka_kaam("Bilal", "sabzi")),
        asyncio.create_task(dost_ka_kaam("Usman", "bread")),
    ]

    for done in asyncio.as_completed(tasks):
        result = await done
        print("📦 Result:", result)

asyncio.run(main())
