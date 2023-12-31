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
import atexit
import signal
# from file_event_listener import EventHandler  

# Add the current directory to the sys.path
sys.path.append(str(parent_dir))

# from handler_event import EventHandler  
from handler_event import HandlerEvent

    

class BloomFilterReader(IAsyncSubject):
    def __init__(self, folder_to_watch=None, time_interval_seconds=5):
        # Create an asyncio event loop
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)

        def callback(src_path):
            self.callback_called = True
            # src_path = Path(src_path).resolve()  # Normalize the path
            print("Notifying Observer/s")
             
            asyncio.run( self.notify("src_path"))

        self._observers = []      
        # runEventHandler(callback)

        

    async def attach(self, observer):
        print(f"{observer} is attached")
        if observer not in self._observers:
            self._observers.append(observer)

    async def detach(self, observer):
        self._observers.remove(observer)

    async def notify(self, message):
        for observer in self._observers:
            await asyncio.gather(*(observer.update(message) for observer in self._observers))

