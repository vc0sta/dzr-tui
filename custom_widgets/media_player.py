from dataclasses import dataclass
from threading import Thread
from time import sleep, strftime, gmtime
import mpv

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
        self.mpv = mpv.MPV()
        
        self.is_playing = False
        self.play_button = self.buttons["none"]

        self.title = ''
        self.artist = ''
        self.album = ''
        self.date = ''

        self.consolidated_info = ""

        self.timeout = 1

        Thread(target=self._monitor_loop, daemon=True).start()


    def _request_data(self) -> PlayerData:
        if self.mpv.metadata != None:
            metadata = self.mpv.metadata  
            
            with open("log.txt", 'w', encoding = 'utf-8') as f:
                f.write(str(metadata))
            self.duration = self.mpv._get_property('duration')
            self.elapsed = self.mpv._get_property('time-pos')

            self.title = metadata.get('title','')
            self.artist = metadata.get('artist','')
            self.album = metadata.get('album','')
            self.date = metadata.get('date','')[:4]

            self.consolidated_info = f"{self.title} - {self.artist} ({self.album} - {self.date})"

            self.is_playing = not self.mpv._get_property('pause')
            self.play_button = self.buttons["pause"] if self.is_playing else self.buttons["play"]

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
        self.mpv._set_property('pause', self.is_playing)
        
    def play(self, media_name):
        self.mpv.play(media_name)
        self.mpv._set_property("pause", False)
        
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