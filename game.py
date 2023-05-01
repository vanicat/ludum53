from collections import OrderedDict
import json
from random import random
from typing import Optional
import arcade
from boat import Boat, BoatView

from const import *

class GameView(arcade.View):
    scene: arcade.Scene
    physics_engine: arcade.PymunkPhysicsEngine
    left_pressed: bool = False
    right_pressed: bool = False
    forward_pressed: bool = False
    backward_pressed: bool = False
    port_pressed: bool = False
    camera: arcade.Camera
    gui_camera: arcade.Camera
    tile_map: arcade.TileMap
    background: arcade.Texture
    dock_inventory: dict

    in_port: Optional[str] = None

    def __init__(self, window):
        """ Create the variables """

        # Init the parent class
        super().__init__(window)

        self.window.set_mouse_visible(False)

        arcade.set_background_color(arcade.color_from_hex_string("#2599c8"))

    def place_camera(self):
        x = max(0, self.player_sprite.center_x - self.camera.viewport_width / 2)
        y = max(0, self.player_sprite.center_y - self.camera.viewport_height / 2)
        self.camera.move_to((x, y), .5)



    def setup(self):
        """ Set up everything with the game """
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING)

        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        self.gui = arcade.Scene()
        self.gui.add_sprite_list("GUI")
        self.roue = arcade.Sprite("assets/roue2.png", 4) 
        self.roue.center_x = self.window.width - 64
        self.roue.center_y = self.window.height - 64
        self.gui.add_sprite("GUI", self.roue)

        layer_options = {
            "Niveau 0": {
                "use_spatial_hash": True,
            },
            "Dessus": {
                "use_spatial_hash": True,
            }
        }

        self.tile_map = arcade.load_tilemap("assets/carte1.tmj", layer_options=layer_options, scaling=2)
        self.background = arcade.load_texture("assets/fond.png")

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list("Player")

        object_layer = self.tile_map.object_lists["objets"]
        self.object_map = { obj.name: obj for obj in object_layer }

        for obj in self.object_map.values():
            if "inventaire" in obj.properties:
                obj.properties["inventaire"] = json.loads(obj.properties["inventaire"])

        self.physics_engine.add_sprite_list(self.scene.get_sprite_list("Niveau 0"),
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.player_sprite = Boat(self.object_map["start"].shape, self.scene, self.physics_engine)

        self.boat_view = BoatView(self.window, self.player_sprite, self.come_back)

        self.force = None

        with open("assets/materiel.json") as f:
            materiels = json.load(f)

        def generate_inventory(dock):
            while True:
                for m in materiels:
                    proba = m["proba"]
                    price = m["base price"]
                    if m["name"] == dock["local"]:
                        proba *= LOCAL_PROB_MULT
                        price *= LOCAL_MULT_PRICE
                    elif m["name"] in dock["distant"]:
                        continue 
                    if random() < proba:
                        v = {
                            "name": m["name"],
                            "value": myround(price * (1 + 0.2 * (random() - 0.5)))
                        }
                        yield v


        self.dock_inventory = {}

        for obj in self.tile_map.object_lists["objets"]:
            if obj.type == "Dock":
                asset = {}
                objects = generate_inventory(obj.properties["inventaire"])
                for i in range(3):
                    for j in range(1, 5):
                        name = f"port trunk {i}{j}"
                        asset[name] = next(objects)
                self.dock_inventory[obj.name] = asset
                

    def come_back(self, ev=None):
        self.window.show_view(self)


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
        elif key == arcade.key.P:
            self.port_pressed = True
        elif key == arcade.key.ESCAPE:
            #TODO: better restarting of a game, with no leak
            self.window.show_menu(self.come_back)

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
        elif key == arcade.key.P:
            self.port_pressed = False

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.my_update(self.left_pressed, self.right_pressed, self.forward_pressed, self.backward_pressed)

        self.physics_engine.step()

        self.in_port = None
        for obj in self.object_map.values():
            if obj.type == "Dock" and arcade.is_point_in_polygon(self.player_sprite.center_x, self.player_sprite.center_y, obj.shape):
                self.in_port = obj

        if self.in_port and self.port_pressed:
            self.port_pressed = False
            self.boat_view.setup(self.in_port, self.dock_inventory[self.in_port.name])
            self.window.show_view(self.boat_view)

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.place_camera()
        self.camera.use()

        arcade.draw_texture_rectangle(
            self.tile_map.width * TILE_SIZE,
            self.tile_map.height * TILE_SIZE,
            self.tile_map.width * TILE_SIZE * 2,
            self.tile_map.height * TILE_SIZE * 2, self.background
        )
        self.scene.draw()

        self.roue.angle = self.player_sprite.barre

        self.gui_camera.use()
        self.gui.draw()

        if self.in_port:
            arcade.draw_text("Press P to dock", 10, self.window.height - 20)

        if self.force:
            x = self.player_sprite.center_x
            y = self.player_sprite.center_y
            arcade.draw_line(x, y, x + self.force.x, y + self.force.y, (200, 0, 100), line_width=3)

