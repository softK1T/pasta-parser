import asyncio
from telethon import TelegramClient, functions, events
from config import config
from database.mongodb import MongoDBClient
from utils.utils import format_messages

# Initialize Telethon client
client = TelegramClient('PastaApp', config.API_ID, config.API_HASH)


async def fetch_messages():
    async with client:
        messages = []
        offset_id = 0

        while True:
            history = await client(functions.messages.GetHistoryRequest(
                peer=config.CHANNEL_USERNAME,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=int(config.HISTORY_LIMIT),
                max_id=0,
                min_id=0,
                hash=0
            ))

            new_messages = history.messages
            if not new_messages:
                break

            messages += new_messages
            offset_id = new_messages[-1].id

            print(f'Fetched {len(new_messages)} messages, current total: {len(messages)}')

            if len(new_messages) < int(config.HISTORY_LIMIT):
                break

        return messages


async def main():
    await client.start()

    messages = await fetch_messages()

    mongo_client = MongoDBClient()

    bulk_messages = format_messages(messages)

    mongo_client.bulk_update_processed_texts(bulk_messages)
    print(f"Total messages processed: {len(bulk_messages)}")

    print(f"Listening to channel: {config.CHANNEL_USERNAME}")


if __name__ == "__main__":
    asyncio.run(main())
