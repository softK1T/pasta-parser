import asyncio
import logging
from utils.mongo_utils import MongoDBClient
from utils.parser_utils import PageParser


async def main():
    mongo_client = MongoDBClient()
    parser = PageParser()

    records = mongo_client.get_urls()
    bulk_updates = []
    records_amount = len(records)
    record_left = records_amount
    print('Records to proceed', records_amount)
    for record in records:
        url = record['pasta_url']
        if url.startswith('https://telegra.ph/'):
            _id = record.get('_id')
            try:
                page_content = parser.fetch_page(url)
                processed_text = parser.parse_page(page_content)
                bulk_updates.append((_id, processed_text))

                record_left -= 1
                print("Processed:", _id, url, "Left", record_left)

            except Exception as e:
                logging.error(e)

    mongo_client.bulk_update_processed_texts(bulk_updates)


if __name__ == '__main__':
    asyncio.run(main())
