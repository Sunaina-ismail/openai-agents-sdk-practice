import asyncio

# Ek simple async function jo pretend karta hai ke kaam kar raha hai
async def banay_chai(nam):
    print(f"{nam} ne chai banana start kiya...")  # Start
    await asyncio.sleep(2)  # Asli kaam — time lag raha hai
    print(f"{nam} ne chai bana li!")  # End
    return f"{nam} ki chai ready hai ☕"

async def main():
    # Step 1: Tasks banaye — lekin abhi run nahi kiye
    tasks = []
    for nam in ["Ali", "Babloo", "Chintu"]:
        task = banay_chai(nam)  # ye coroutine object hai, run nahi hua abhi
        tasks.append(task)

    # Step 2: Ab sab ko ek saath run karo using gather
    results = await asyncio.gather(*tasks)

    # Step 3: Result print karo
    for chai in results:
        print(chai)

# Run the async main
asyncio.run(main())
