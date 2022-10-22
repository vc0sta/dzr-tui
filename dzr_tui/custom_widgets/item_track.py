from dataclasses import dataclass
from threading import Thread
from time import sleep
from time import strftime, gmtime
import os

from pytermgui import Container, StyleManager, real_length, tim, Button, Splitter

from .downloader import DLR
from threading import Thread
from deezer import Deezer

client = Deezer()

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
        "play":  "▶",
        "download": "↓"
    }

    def __init__(self, media_player, data, **attrs) -> None:
        super().__init__(**attrs)
        self.id = data["id"]
        self.title = data["title"]
        self.link = data["link"]
        self.artist_name = data["artist"]["name"],
        self.artist_link = data["artist"]["link"]
        self.album = data["album"]
        self.track_number = '00'

        self.media_player = media_player

        # Display everything
        self.update_content()

    def download(self):
        download_manager = DLR(portable=True)
        # TODO: The bitrate/location should be defined by the end-user (TUI)
        #      Maybe some queue should be created as well to deal with multiple downloads
        #      downloader.py already has such funcionality, this should be considered while merging.
        download_manager.loadLinks(url=[self.link], bitrate="320")
        download_manager.getsongs()

    def play(self):
        album_tracks = client.api.get_album_tracks(self.album['id'])
        track_info = next((item for item in album_tracks['data'] if item['id'] == self.id), None)
        
        self.track_number = track_info['track_position']

        # TODO: Understand why artist_name is a Tuple
        #   (keep in mind that this is a temp approach and play() should work with streaming)

        file_name = "./music/{artist_name}/{album_name}/{track_number:02d} - {title}.mp3".format(
            artist_name=self.artist_name[0],
            album_name=self.album['title'],
            track_number=self.track_number,
            title=self.title
        )

        if os.path.exists(file_name):
            self.media_player.play(file_name)
        
    def update_content(self) -> None:
        self.set_widgets(
            [   
                Splitter(
                    self.title,
                    self.artist_name,
                    self.album["title"],
                    Splitter(
                        Button(self.buttons["play"], lambda *_: self.play()),
                        Button(self.buttons["download"], lambda *_: self.download()))
                )             
                
            ]
        )