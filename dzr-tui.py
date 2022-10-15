from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace

import pytermgui as ptg


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

    ptg.boxes.SINGLE.set_chars_of(ptg.Window)


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


    # A slot in the same row as body, using the full non-occupied height and
    # 20% of the terminal's height.
    layout.add_slot("Body right", width=0.2)

    # A body slot that will fill the entire width, and the height is remaining
    layout.add_slot("Body")
    

    layout.add_break()

    # A footer with a static height of 1
    layout.add_slot("Player control", height=4, width=0.2)
    layout.add_slot("Player info", height=4)

    return layout


def main(argv: list[str] | None = None) -> None:
    """Runs the application."""

    _create_aliases()
    _configure_widgets()

    args = _process_arguments(argv)

    with ptg.WindowManager() as manager:
        manager.layout = _define_layout()

        search = ptg.Window(
                    ptg.Splitter(
                        ptg.InputField(value="artist|album|track", prompt="Search:"),
                        ptg.Button("Search", lambda *_: manager.stop())
                    )
                , box="EMPTY")
        
        user_menu = ptg.Window(
            ptg.Splitter(
                ptg.Button("User", lambda *_: manager.stop()),
                ptg.Button("Close", lambda *_: manager.stop()),
            ),
            box="EMPTY"
        )
            
        # Since search is the first defined slot, this will assign to the correct place
        manager.add(search, assign="search_bar")
        manager.add(user_menu, assign="user_menu")

        left_menu = ptg.Window(
                ptg.Button("Music", lambda *_: manager.stop()),
                "",
                ptg.Button("Podcasts", lambda *_: manager.stop()),
                "",
                ptg.Button("Favorites", lambda *_: manager.stop()),
            box="SINGLE"
            )

        player_control = ptg.Window(
            ptg.Splitter( 
                "|<",
                ">",
                ">|"
            ),
            box="SINGLE"
        )

        player_info = ptg.Window(
                ptg.Container(
                    "The Metal - Tenacious D",
                    ptg.Splitter(
                        "00:05",
                        ptg.Slider(min_width=10),
                        "02:46"
                    ),                
                ),
            box="EMPTY"
        )

        # Since the second slot, body was not assigned to, we need to manually assign
        # to "player"
        manager.add(player_control, assign="player_control")
        manager.add(player_info, assign="player_info")

        manager.add(left_menu, assign="body_right")
        manager.add(ptg.Window("My body window"), assign="body")

    # ptg.tim.print("")


if __name__ == "__main__":
    main(sys.argv[1:])