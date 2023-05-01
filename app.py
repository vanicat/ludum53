import arcade
import arcade.gui
from typing import Optional
import math
from arcade.application import Window
import pymunk
import json

from boat import Boat, BoatView
from game import GameView
from const import *

class GameWindow(arcade.Window):
    """ Main Window """

    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.my_music = arcade.load_sound("assets/music/music-wave.wav")
        self.media_player = self.my_music.play(loop=True)

        self.menu = Menu(self)


    def music_over(self):
        self.my_music.stop(self.media_player)
        self.media_player.pop_handlers()
        self.media_player = self.my_music.play()
        self.media_player.push_handlers(on_eos=self.my_music.play)

    def show_menu(self, go_back = None):
        if go_back is None:
            self.show_view(self.menu)
        else:
            self.show_view(Menu(self, go_back))


class Menu(arcade.View):
    def __init__(self, window: GameWindow, go_back = None):
        super().__init__(window)

        self.media_player = window.media_player

        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))
        start_button.on_click = self.start_game # type: ignore[method-assign]

        if go_back:
            continue_button = arcade.gui.UIFlatButton(text="Continue", width=200)
            self.v_box.add(continue_button.with_space_around(bottom=20))
            continue_button.on_click = go_back # type: ignore[method-assign]

        more_volume_button = arcade.gui.UIFlatButton(text="More Music", width=200)
        self.v_box.add(more_volume_button.with_space_around(bottom=20))
        more_volume_button.on_click = self.more_volume # type: ignore[method-assign]

        less_volume_button = arcade.gui.UIFlatButton(text="Less Music", width=200)
        self.v_box.add(less_volume_button.with_space_around(bottom=20))
        less_volume_button.on_click = self.less_volume # type: ignore[method-assign]

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))
        quit_button.on_click = self.quit  # type: ignore[method-assign]

        self.text = arcade.Text("""
Use :
  - a/s to accelerate/brake
  - w/d to steer the well
  - ESC for pause/restart""", start_x=900, start_y=400, multiline=True, width = 400)

        self.manager.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box)
        )

    def less_volume(self, event):
        v = self.media_player.volume
        v = max(0, v - 0.1)
        self.media_player.volume = v

    def more_volume(self, event):
        v = self.media_player.volume
        v = min(1, v + 0.1)
        self.media_player.volume = v

    def start_game(self, event):
        start_game(self.window)

    def quit(self, event):
        arcade.exit()

    def on_hide_view(self):
        self.manager.disable()
        self.window.set_mouse_visible(False)
        return super().on_hide_view()
    
    def on_show_view(self):
        self.manager.enable()
        self.window.set_mouse_visible(True)
        return super().on_show_view()
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.text.draw()

def start_game(window):
    start_view = GameView(window)
    window.show_view(start_view)
    start_view.setup()


def main():
    """ Main function """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_menu()
    arcade.run()


if __name__ == "__main__":
    main()