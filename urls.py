import asyncio
import httpx

urls = [
    "https://www.google.com",
    "https://github.com",
    "https://openai.com",
    "https://python.org",
    "https://thiswebsitedoesnotexist123456.com"
]

async def check_urls():

    async with httpx.AsyncClient() as client:

        for u in urls:

            try:
                response = await client.get(u)
                print(u, "-->", response.status_code)

            except httpx.RequestError:
                print(u, "--> Unable to connect")

asyncio.run(check_urls())    