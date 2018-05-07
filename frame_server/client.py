import asyncio
import random

last_message = None

# This function has driving code
async def drive(loop):
    global last_message
    while True:
        await asyncio.sleep(1.0, loop)
        # last_message should contain result of processed camera frames. do something with it
        print("last_message", last_message)

# This function sends camera frames to server
async def send_frames(message, loop):
    global last_message
    while True:
        await asyncio.sleep(3.0, loop)
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888, loop=loop)
        writer.write(message.encode())
        data = await reader.read(100)
        last_message = data.decode()
        writer.close()

message = 'Hello World {}'.format(random.randint(1, 10))
loop = asyncio.get_event_loop()
# Create coroutines for each simultaneous task
sender_coro = send_frames(message, loop)
drive_coro = drive(loop)
# Create a simultaneous task
task = loop.create_task(asyncio.gather(sender_coro, drive_coro))

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
