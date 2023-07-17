from packages.bitpanda.BitpandaClient import BitpandaClient


class AsyncBitpandaClient(BitpandaClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
