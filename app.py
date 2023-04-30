import arcade
import math
import pymunk

from boat import Boat
from const import *

class GameWindow(arcade.Window):
    """ Main Window """

    scene: arcade.Scene
    physics_engine: arcade.PymunkPhysicsEngine
    left_pressed: bool
    right_pressed: bool
    forward_pressed: bool
    backward_pressed: bool
    camera: arcade.Camera
    gui_camera: arcade.Camera
    tile_map = arcade.TileMap
    background = arcade.Texture

    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def place_camera(self):
        x = max(0, self.player_sprite.center_x - self.camera.viewport_width / 2)
        y = max(0, self.player_sprite.center_y - self.camera.viewport_height / 2)
        self.camera.move_to((x, y), .5)



    def setup(self):
        """ Set up everything with the game """
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING)

        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        self.gui = arcade.Scene()
        self.gui.add_sprite_list("GUI")
        self.roue = arcade.Sprite("assets/roue2.png", 4) 
        self.roue.center_x = self.width - 64
        self.roue.center_y = self.height - 64
        self.gui.add_sprite("GUI", self.roue)

        layer_options = {
            "Niveau 0": {
                "use_spatial_hash": True,
            },
            "Dessus": {
                "use_spatial_hash": True,
            }
        }

        self.tile_map = arcade.load_tilemap("assets/carte1.tmx", layer_options=layer_options)
        self.background = arcade.load_texture("assets/fond.png")

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list("Player")

        object_layer = self.tile_map.object_lists["objets"]
        self.object_map = { obj.name: obj for obj in object_layer }

        self.physics_engine.add_sprite_list(self.scene.get_sprite_list("Niveau 0"),
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.player_sprite = Boat(self.object_map["start"].shape, self.scene, self.physics_engine)

        self.left_pressed = False
        self.right_pressed =  False
        self.forward_pressed = False
        self.backward_pressed = False
        self.force = None


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.forward_pressed = True
        elif key == arcade.key.DOWN:
            self.backward_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.forward_pressed = False
        elif key == arcade.key.DOWN:
            self.backward_pressed = False

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.my_update(self.left_pressed, self.right_pressed, self.forward_pressed, self.backward_pressed)

        self.physics_engine.step()

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.place_camera()
        self.camera.use()

        arcade.draw_texture_rectangle(self.tile_map.width * TILE_SIZE/2, self.tile_map.height * TILE_SIZE/2, self.tile_map.width * TILE_SIZE, self.tile_map.height * TILE_SIZE, self.background)
        self.scene.draw()

        self.roue.angle = self.player_sprite.barre

        self.gui_camera.use()
        self.gui.draw()

        if self.force:
            x = self.player_sprite.center_x
            y = self.player_sprite.center_y
            arcade.draw_line(x, y, x + self.force.x, y + self.force.y, (200, 0, 100), line_width=3)



def main():
    """ Main function """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()