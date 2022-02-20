from config import bot
#from bot import handle
import asyncio
import scenario

async def main():
	await bot.long_polling()

loop = asyncio.get_event_loop()
task = loop.create_task(main())

try:
	loop.run_until_complete(task)
	#asyncio.run(main())
except KeyboardInterrupt as e:
	task.cancel()
	task.exception()
#finally:
loop.close()