from dataclasses import dataclass
from threading import Thread
from time import sleep, strftime, gmtime
from mpd import MPDClient

from pytermgui import Container, Button, StyleManager, real_length, tim, Splitter, Slider

@dataclass
class PlayerData:
    track: str
    artist: str
    album: str
    date: str
    is_playing: bool

class Player(Container):
    buttons = {
        "play":  "▶",
        "pause": "⏸",
        "none": ""
    }

    def __init__(self, **attrs) -> None:
        super().__init__(**attrs)
        self.mpd = MPDClient()
        self.mpd.connect("localhost", 6600)
        
        self.is_playing = False
        self.play_button = self.buttons["none"]

        self.title = ''
        self.artist = ''
        self.album = ''
        self.date = ''

        self.consolidated_info = ""

        self.timeout = 10

        Thread(target=self._monitor_loop, daemon=True).start()


    def _request_data(self) -> PlayerData:
        # try:
        #     metadata = self.mpd.currentsong()
        # except:
        metadata = self.mpd.currentsong()
        status = self.mpd.status()
        
        if metadata != {}:
            
            self.elapsed = float(status.get('elapsed', '0'))
            self.duration = float(status.get('duration', '0'))

            self.title = metadata.get('title','')
            self.artist = metadata.get('artist','')
            self.album = metadata.get('album','')
            # self.date = metadata.get('date','')[:4]

            self.consolidated_info = f"{self.title} - {self.artist} ({self.album})"

            self.state = self.mpd.status()['state']
            
            if self.state == 'play':
                self.play_button = self.buttons.get('pause')
            else:
                self.play_button = self.buttons.get('play')

        else:
            self.duration = 1
            self.elapsed = 1

            self.title = ""
            self.artist = ""
            self.album = ""
            self.date = ""

            self.consolidated_info = ""

            self.play_button = self.buttons["none"]

        
    def _monitor_loop(self) -> None:
        while True:
            self._request_data()
            self.update_content()
            sleep(self.timeout)

    def _press_play_button(self):
        self.mpd.pause() if self.state == 'play' else self.mpd.play()
        pass
        
    def play(self):
        # self.mpd.play()
        pass
        
    def update_content(self) -> None:
        self.set_widgets(
            [                
                    self.consolidated_info,
                    Splitter(
                        Button(self.play_button, lambda *_: self._press_play_button()),
                        strftime("%M:%S", gmtime(self.elapsed)), 
                        Slider(), 
                        strftime("%M:%S", gmtime(self.duration))
                    )
            ]
        )