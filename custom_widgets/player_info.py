from dataclasses import dataclass
from threading import Thread
from time import sleep


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

        self.timeout = 1

        Thread(target=self._monitor_loop, daemon=True).start()


    def _request_data(self) -> PlayerInfoData:
        metadata = self.player.metadata if self.player.metadata != None else {"title": "", "artist": "", "album": "", "date": "" }

            
        self.title = metadata['title']
        self.artist = metadata['artist']
        self.album = metadata['album']
        self.date = metadata['date']

    def _monitor_loop(self) -> None:
        while True:
            self._request_data()
            self.update_content()
            sleep(self.timeout)
            
    def update_content(self) -> None:
        self.set_widgets(
            [                
                    f"{self.title} - {self.artist} ({self.album} - {self.date})",
                    Splitter("00:00", Slider(), "00:00"), 
            ]
        )