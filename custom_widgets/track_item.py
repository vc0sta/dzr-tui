from dataclasses import dataclass
from threading import Thread
from time import sleep
from time import strftime, gmtime

from pytermgui import Container, StyleManager, real_length, tim, Button, Splitter

from .downloader import DLR

@dataclass
class TrackData:
    id: int
    title: str
    link: str
    artist_name: str
    artist_link: str
    album: str

class Track(Container):
    buttons = {
        "play":  "▶"
    }

    def __init__(self, player_wrapper, data, **attrs) -> None:
        super().__init__(**attrs)
        self.id = data["id"]
        self.title = data["title"]
        self.link = data["link"]
        self.artist_name = data["artist"]["name"],
        self.artist_link = data["artist"]["link"]
        self.album = data["album"]["title"]

        self.player_wrapper = player_wrapper

        # Display everything
        self.update_content()

    def _press_play_button(self):
        # download_manager = DLR(portable=None)
        # download_manager.loadLinks(url=[self.link], bitrate="320")
        self.player_wrapper.play_media('music.mp3')

    def update_content(self) -> None:
        self.set_widgets(
            [   
                Splitter(
                    self.title,
                    self.artist_name,
                    self.album,
                    Button(self.buttons["play"], lambda *_: self._press_play_button())
                )             
                
            ]
        )