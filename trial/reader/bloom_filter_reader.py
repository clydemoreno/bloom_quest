import sys
# sys.path.append("../messaging")

sys.path.append('./async')

from pathlib import Path
parent_dir = Path(__file__).resolve().parent
# print (parent_dir.parent)
# Add the 'messaging' directory to sys.path
sys.path.append(str(parent_dir.parent / 'messaging'))

from IAsyncSubject import IAsyncSubject

import asyncio

from file_event_listener import EventHandler  

parent_dir = Path(__file__).resolve().parent

class BloomFilterReader(IAsyncSubject):
    def __init__(self,folder_to_watch):
        def callback(src_path):
            self.callback_called = True
            src_path = Path(src_path).resolve()  # Normalize the path
            print("Notifying Observer/s")
             
            asyncio.run( self.notify(src_path))

        self._observers = []
        self.file_listener = EventHandler(folder_to_watch, callback)
        

    async def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    async def detach(self, observer):
        self._observers.remove(observer)

    async def notify(self, message):
        for observer in self._observers:
            await asyncio.gather(*(observer.update(message) for observer in self._observers))




# from IAsyncSubject import IAsyncSubject
# import asyncio

# class AsyncConcreteSubject(IAsyncSubject):
    # async def notify(self, message):
    #     await asyncio.gather(*(observer.update(message) for observer in self._observers))
