from dataclasses import dataclass
from threading import Thread
from time import sleep
from time import strftime, gmtime

from pytermgui import Container, StyleManager, real_length, tim, Button

@dataclass
class PlayerControlData:
    is_playing: bool

class PlayerControl(Container):
    buttons = {
        "play":  "▶",
        "pause": "⏸"
    }

    def __init__(self, player, **attrs) -> None:
        super().__init__(**attrs)
        self.is_playing = False
        self.player = player

        self.play_button = self.buttons["play"]
        self.update_content()

    def _request_data(self) -> PlayerControlData:
        self.is_playing = self.player._get_property('pause')

    def _press_play_button(self):
        self._request_data()
        self.player._set_property('pause', not self.is_playing)
        self.update_content()

    def update_content(self) -> None:
        self.play_button = self.buttons["pause"] if self.is_playing else self.buttons["play"]
        self.set_widgets(
            [                
                Button(self.play_button, lambda *_: self._press_play_button())
            ]
        )