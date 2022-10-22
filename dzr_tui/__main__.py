#!/usr/bin/env python3
from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace

import pytermgui as ptg

from custom_widgets.media_player import Player
from custom_widgets.item_track import Track
from custom_widgets.item_artist import Artist
from custom_widgets.item_album import Album

import configparser

from deezer import Deezer

client = Deezer()
player_wrapper = Player()

welcome_message = """
██████╗ ███████╗██████╗        ██████╗██╗     ██╗
██╔══██╗╚══███╔╝██╔══██╗      ██╔════╝██║     ██║
██║  ██║  ███╔╝ ██████╔╝█████╗██║     ██║     ██║
██║  ██║ ███╔╝  ██╔══██╗╚════╝██║     ██║     ██║
██████╔╝███████╗██║  ██║      ╚██████╗███████╗██║
╚═════╝ ╚══════╝╚═╝  ╚═╝       ╚═════╝╚══════╝╚═╝

THE TERMINAL DEEZER CLIENT

To use download feature, you must have a valid .arl in your config folder.
Check the README.md for instructions.
"""


def _process_arguments(argv: list[str] | None = None) -> Namespace:
    """Processes command line arguments.
    Note that you don't _have to_ use the bultin argparse module for this; it
    is just what the module uses.
    Args:
        argv: A list of command line arguments, not including the binary path
            (sys.argv[0]).
    """

    parser = ArgumentParser(description="My first PTG application.")

    return parser.parse_args(argv)


def _create_aliases() -> None:
    """Creates all the TIM aliases used by the application.
    Aliases should generally follow the following format:
        namespace.item
    For example, the title color of an app named "myapp" could be something like:
        myapp.title
    """


def _configure_widgets() -> None:
    """Defines all the global widget configurations.
    Some example lines you could use here:
        ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
        ptg.Splitter.set_char("separator", " ")
        ptg.Button.styles.label = "myapp.button.label"
        ptg.Container.styles.border__corner = "myapp.border"
    """
    ptg.Button.set_char("delimiter", [""] * 2)
    # ptg.boxes.SINGLE.set_chars_of(ptg.Window)


def _define_layout() -> ptg.Layout:
    """Defines the application layout.
    Layouts work based on "slots" within them. Each slot can be given dimensions for
    both width and height. Integer values are interpreted to mean a static width, float
    values will be used to "scale" the relevant terminal dimension, and giving nothing
    will allow PTG to calculate the corrent dimension.
    """

    layout = ptg.Layout()

    # A header slot with a height of 1
    layout.add_slot("Search bar", height=1)
    layout.add_slot("User menu", height=1, width=0.2)
    layout.add_break()

    # A body slot that will fill the entire width, and the height
    layout.add_slot("Body")

    layout.add_break()

    # A footer with a static height of 1
    layout.add_slot("Player", height=4)

    # layout.add_slot("Player control", height=4, width=0.2)
    # layout.add_slot("Player info", height=4)

    return layout


def search_for(query, body, window_manager, filter_by=""):
    if query != "":
        if filter_by == 'track':
            response = client.api.search_track(query)
        elif filter_by == 'artist':
            response = client.api.search_artist(query)
        elif filter_by == 'album':
            response = client.api.search_album(query)
        else:
            response = client.api.search(query)

        widgets = []
        for data in response['data']:
            if data['type'] == 'track':
                widgets.append(
                    Track(player_wrapper, data, box="EMPTY")
                )
            elif data['type'] == 'artist':
                widgets.append(
                    Artist(data, window_manager, box="EMPTY")
                )
            elif data['type'] == 'album':
                widgets.append(
                    Album(data, window_manager, box="EMPTY")
                )
            widgets.append("")

        body.set_widgets(widgets)


def main(argv: list[str] | None = None) -> None:
    """Runs the application."""

    _create_aliases()
    _configure_widgets()

    args = _process_arguments(argv)

    with ptg.WindowManager() as manager:
        manager.layout = _define_layout()

        search_input = ptg.InputField(value="", prompt="[primary]Search for: ")

        body_content = ptg.Container(welcome_message)
        body_window = ptg.Window(body_content, box='EMPTY')

        search = ptg.Window(
            ptg.Splitter(
                search_input,
                ptg.Splitter(
                    "[primary]Filter by:",
                    ptg.Button(
                        " Track ", lambda *_: search_for(search_input.value, body_content, manager, 'track')),
                    ptg.Button(
                        " Artist ", lambda *_: search_for(search_input.value, body_content, manager, 'artist')),
                    ptg.Button(
                        " Album ", lambda *_: search_for(search_input.value, body_content, manager, 'album'))
                )
            ), box="EMPTY")

        user_menu = ptg.Window(
            ptg.Splitter(
                # ptg.Button("User", lambda *_: manager.stop()),
                ptg.Button(" Close ", lambda *_: manager.stop()),
            ),
            box="EMPTY"
        )

        # Since search is the first defined slot, this will assign to the correct place
        manager.add(search, assign="search_bar")
        manager.add(user_menu, assign="user_menu")

        player = ptg.Window(player_wrapper, box="EMPTY")

        manager.add(body_window, assign="body")

        manager.add(player, assign="player")

    ptg.tim.print("Application closed.")


if __name__ == "__main__":
    main(sys.argv[1:])
