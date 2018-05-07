import asyncio
import random
import pickle

loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)

async def process_frames(queue):
    while True:
        data, writer = await queue.get()
        nparray = pickle.loads(data)
        print("Processing: ", nparray.shape)
        # Calculate frame result
        result = "Result: {}".format(random.randint(20, 30))
        writer.write(result.encode())
        await writer.drain()

async def receive_frames(reader, writer):
    global queue
    data = await reader.read(40000)
    addr = writer.get_extra_info('peername')
    print("Received frame from: ", addr)
    await queue.put((data, writer))

receive_coro = asyncio.start_server(receive_frames, '127.0.0.1', 8888, loop=loop)
process_coro = process_frames(queue)
server = loop.run_until_complete(asyncio.gather(receive_coro, process_coro))

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
