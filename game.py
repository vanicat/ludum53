from collections import OrderedDict
import json
from random import choice, random
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
        self.roue_dir = arcade.Sprite("assets/roue2-direction.png", 4) 
        self.roue_dir.center_x = self.window.width - 64
        self.roue_dir.center_y = self.window.height - 64 - 5
        self.roue = arcade.Sprite("assets/roue2.png", 4) 
        self.roue.center_x = self.window.width - 64
        self.roue.center_y = self.window.height - 64 - 15
        self.docking_message = arcade.Text("Press P to dock", start_x=self.roue.left, start_y=self.roue.top,
                                           anchor_x="right", anchor_y="top")
        self.fuel_message = arcade.Text("fuel: XXXXXX", self.docking_message.left, self.docking_message.bottom,
                                        anchor_x="left", anchor_y="top")
        self.money_message = arcade.Text("money: XXXXXX", self.fuel_message.left, self.fuel_message.bottom,
                                          anchor_x="left", anchor_y="top")
        sx = self.docking_message.left - 10
        sy = self.window.height
        ex = self.window.width
        ey = self.roue.bottom - 10
        self.gui_rectangle = [(sx, sy), (sx, ey), (ex, ey), (ex, sy)]
        self.gui.add_sprite("GUI", self.roue)
        self.gui.add_sprite("GUI", self.roue_dir)

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

        def generate_inventory(dock, market):
            while True:
                m = choice(materiels)
                proba = m["proba"]
                price = m["base price"]
                if m["name"] == dock["local"]:
                    proba *= LOCAL_PROB_MULT
                    price *= LOCAL_MULT_PRICE
                elif m["name"] in dock["distant"]:
                    continue 
                if random() < proba:
                    price = myround(price * (1 + 0.2 * (random() - 0.5)))
                    if price > market[m["name"]]:
                        v = {
                            "name": m["name"],
                            "value": price
                        }
                        yield v


        self.dock_inventory = {}
        self.dock_market = {}

        for obj in self.tile_map.object_lists["objets"]:
            if obj.type == "Dock":
                market = OrderedDict()
                for m in materiels:
                    price = m["base price"]
                    if m["name"] == obj.properties["inventaire"]["local"]:
                        price *= 0
                    elif m["name"] in obj.properties["inventaire"]["distant"]:
                        price *= DIST_MULT_PRICE

                    price *= 1 + 0.2 * (random() - 0.7)
                    market[m["name"]] = myround(price)

                self.dock_market[obj.name] = market

                asset = {}
                objects = generate_inventory(obj.properties["inventaire"], market)
                for i in range(3):
                    for j in range(1, 5):
                        name = f"port trunk {i}{j}"
                        asset[name] = next(objects)
                self.dock_inventory[obj.name] = asset
    

    def come_back(self, ev=None):
        self.window.show_view(self)


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.UP or key == arcade.key.W:
            self.forward_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.backward_pressed = True
        elif key == arcade.key.P:
            self.port_pressed = True
        elif key == arcade.key.ESCAPE:
            #TODO: better restarting of a game, with no leak
            self.window.show_menu(self.come_back)


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.UP or key == arcade.key.W:
            self.forward_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
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
            self.boat_view.setup(self.in_port, self.dock_inventory[self.in_port.name], self.dock_market[self.in_port.name])
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
        arcade.draw_polygon_filled(self.gui_rectangle, arcade.csscolor.BLACK)
        self.gui.draw()

        if self.in_port:
            self.docking_message.draw()

        if self.force:
            x = self.player_sprite.center_x
            y = self.player_sprite.center_y
            arcade.draw_line(x, y, x + self.force.x, y + self.force.y, (200, 0, 100), line_width=3)

