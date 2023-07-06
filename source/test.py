import asyncio
import aiohttp


async def make_request():
    async with aiohttp.ClientSession() as session:
        # Perform your HTTP request(s) here

        # Example GET request
        async with session.get('https://example.com') as response:
            data = await response.text()
            print(data)


# Run the event loop to execute the function
loop = asyncio.get_event_loop()
loop.run_until_complete(make_request())

# Close the event loop after execution
loop.close()
