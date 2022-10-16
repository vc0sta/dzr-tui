from dataclasses import dataclass
from threading import Thread
from time import sleep
from time import strftime, gmtime

from pytermgui import Container, StyleManager, real_length, tim, Button, Splitter

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

    def __init__(self, data, **attrs) -> None:
        super().__init__(**attrs)
        self.id = data["id"]
        self.title = data["title"]
        self.link = data["link"]
        self.artist_name = data["artist"]["name"],
        self.artist_link = data["artist"]["link"]
        self.album = data["album"]["title"]

        # Display everything
        self.update_content()

    def _press_play_button(self):
        # Donwload then play song
        pass

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