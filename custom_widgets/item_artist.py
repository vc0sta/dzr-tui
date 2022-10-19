from pytermgui import Container, StyleManager, real_length, tim, Button, Splitter
from dataclasses import dataclass

@dataclass
class ArtistData:
    id: int
    name: str
    link: str

class Artist(Container):
    def __init__(self, data, **attrs) -> None:
        super().__init__(**attrs)
        self.id = data["id"]
        self.name = data["name"]
        self.link = data["link"]

        self.update_content()

    def update_content(self) -> None:
        self.set_widgets(
            [   
                Splitter(
                    str(self.id),
                    self.name,
                    self.link
                )             
                
            ]
        )