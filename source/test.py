import asyncio
import aiohttp
import keys
from packages.bitpanda.BitpandaClient import BitpandaClient


class AsyncBitpandaClient(BitpandaClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()


async def make_request():
    client = BitpandaClient(keys.KEY_TRADE)
    client = AsyncBitpandaClient(client)
    async with client as session:
        # Perform your HTTP request(s) here

        # Example GET request using the modified BitPanda client instance
        instruments_response = await session.get_instruments()

        print(instruments_response)


# Run the event loop to execute the function
loop = asyncio.get_event_loop()
loop.run_until_complete(make_request())

# Close the event loop after execution
loop.close()