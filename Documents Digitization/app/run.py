import asyncio
import consumer

# from utils.config import logger


loop = asyncio.get_event_loop()
print(loop)

loop.run_until_complete(consumer.main())
