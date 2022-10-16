from dataclasses import dataclass
from threading import Thread
from time import sleep
from time import strftime, gmtime

from pytermgui import Container, StyleManager, real_length, tim, Splitter, Slider

@dataclass
class PlayerInfoData:
    track: str
    artist: str
    album: str
    date: str


class PlayerInfo(Container):
    def __init__(self, player, **attrs) -> None:
        super().__init__(**attrs)
        
        self.player = player

        self.title = ''
        self.artist = ''
        self.album = ''
        self.date = ''

        self.consolidated_info = ""

        self.timeout = 1

        Thread(target=self._monitor_loop, daemon=True).start()


    def _request_data(self) -> PlayerInfoData:
        if self.player.metadata != None:
            metadata = self.player.metadata  
            
            self.duration = self.player._get_property('duration')
            self.elapsed = self.player._get_property('time-pos')

            self.title = metadata['title']
            self.artist = metadata['artist']
            self.album = metadata['album']
            self.date = metadata['date']

            self.consolidated_info = f"{self.title} - {self.artist} ({self.album} - {self.date})"

        else:
            self.duration = 0
            self.elapsed = 1

            self.title = ""
            self.artist = ""
            self.album = ""
            self.date = ""

            self.consolidated_info = ""


    def _monitor_loop(self) -> None:
        while True:
            self._request_data()
            self.update_content()
            sleep(self.timeout)
            
    def update_content(self) -> None:
        self.set_widgets(
            [                
                    self.consolidated_info,
                    Splitter(strftime("%M:%S", gmtime(self.elapsed)), 
                    Slider(value=self.duration/self.elapsed), 
                    strftime("%M:%S", gmtime(self.duration)))
            ]
        )