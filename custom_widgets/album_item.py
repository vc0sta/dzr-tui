from dataclasses import dataclass
from threading import Thread
from time import sleep
from time import strftime, gmtime

from pytermgui import Container, StyleManager, real_length, tim, Button, Splitter

from .downloader import DLR

@dataclass
class AlbumData:
    id: int
    title: str
    link: str
    artist_name: str
    artist_link: str
    tracklist: str

class Album(Container):
    buttons = {
        "play":  "▶",
        "download": "↓"
    }
    def __init__(self, data, **attrs) -> None:
        super().__init__(**attrs)
        self.id = data["id"]
        self.title = data["title"]
        self.link = data["link"]
        self.artist_name = data["artist"]["name"],
        self.artist_link = data["artist"]["link"]
        self.tracklist = data["tracklist"]

        # Display everything
        self.update_content()

    def do_nothing():
        pass
    
    def update_content(self) -> None:
        self.set_widgets(
            [   
                Splitter(
                    self.title,
                    self.artist_name,
                    self.link,
                    Splitter(
                        Button(self.buttons["play"], lambda *_: self.do_nothing()),
                        Button(self.buttons["download"], lambda *_: self.do_nothing()))
                )             
                
            ]
        )