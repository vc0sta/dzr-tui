from dataclasses import dataclass
from threading import Thread
from time import sleep
from time import strftime, gmtime

from pytermgui import Container, StyleManager, real_length, tim, Button, Splitter, InputField, Window
from deezer import Deezer

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
    def __init__(self, data, window_manager, **attrs) -> None:
        super().__init__(**attrs)
        self.id = data["id"]
        self.title = data["title"]
        self.link = data["link"]
        self.artist_name = data["artist"]["name"],
        # self.artist_link = data["artist"]["link"]
        self.tracklist = data["tracklist"]
        self.window_manager = window_manager

        # Display everything
        self.update_content()

    def show_album(self):
        client = Deezer()
        
        tracklist = client.api.get_album_tracks(self.id)

        tracks_widgets = []
        for track in tracklist['data']:
            tracks_widgets.append(
                Splitter(
                    track.get('title', ''),
                    f"{track.get('track_position', ''):02d}",
                    strftime("%M:%S", gmtime(track.get('duration'))),
                    Button(self.buttons["play"]),
                    Button(self.buttons["download"])
                )
            )
            tracks_widgets.append("")

        tracklist = Container() 
        tracklist.set_widgets(tracks_widgets)

        window = (
            Window(
                "",
                InputField(self.title, prompt="Title: "),
                InputField(self.artist_name[0], prompt="Artist: "),
                # InputField(self.tracklist, prompt="Tracklist: "),
                "",
                tracklist,
                "",
                ["Close", lambda *_: window.close()],
                width=150,
                box="DOUBLE",
            )
            .set_title(f"[210 bold] {self.title}")
            .center()
        )

        self.window_manager.add(window)
        
    
    def update_content(self) -> None:
        self.set_widgets(
            [   
                Splitter(
                    self.title,
                    self.artist_name,
                    # self.link,
                    Splitter(
                        Button(self.buttons["play"], lambda *_: self.show_album()),
                        Button(self.buttons["download"], lambda *_: self.do_nothing()))
                )             
                
            ]
        )