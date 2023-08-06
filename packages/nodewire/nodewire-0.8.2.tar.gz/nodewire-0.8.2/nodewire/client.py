import asyncio

class client():
    def __init__(self):
        self.reader = None
        self.writer = None
        self.received = None

    async def connect(self,loop, serverHost='dashboard.nodewire.org'):
        self.reader, self.writer = await asyncio.open_connection(serverHost, 10001, loop=loop)
        while True:
            try:
                data = await self.reader.readline()
                if len(data)==0 and self.received:
                    self.received('disconnected')
                    break
                if self.received:
                    try:
                        self.received(data.decode().strip())
                    except Exception as ex1:
                        print(str(ex1))
            except Exception as ex:
                print(str(ex))
                if self.received:
                    self.received('disconnected')
                break
        print('Close the socket')
        self.writer.close()
        asyncio.get_event_loop().close()
        asyncio.get_event_loop().stop()


    async def sendasync(self, message):
        while(self.writer==None): await asyncio.sleep(1)
        self.writer.write(message.encode())

    def send(self, message):
        try:
            self.writer.write(message.encode())
        except:
            # todo
            self.writer.close()
            print("failed to send")

if __name__ == '__main__':
    c = client()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(c.connect(loop))
    except KeyboardInterrupt:
        pass
    loop.close()