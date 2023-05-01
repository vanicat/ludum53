from typing import Optional
from arcade.application import Window
import pymunk
import arcade

from const import *

class Boat(arcade.Sprite):
    camera: arcade.Camera
    physics_engine: arcade.PymunkPhysicsEngine
    physique_body: pymunk.Body
    barre: float
    inventaire: dict
    money: float
    fuel: float

    def __init__(self, pos:tuple[float, float], scene:arcade.Scene, engine:arcade.PymunkPhysicsEngine):
        super().__init__("assets/boat.png", 2)
        self.center_x = pos[0]
        self.center_y = pos[1]
        scene.add_sprite("Player", self)
        self.physics_engine = engine

        self.physics_engine.add_sprite(self,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       collision_type="player",
                                       max_velocity=PLAYER_MAX_SPEED
                                      )
        body = self.physics_engine.sprites[self].body
        assert body is not None
        self.physique_body = body

        self.barre = 0

        self.inventaire = {}
        for i in range(4):
            for j in range(3):
                self.inventaire[f"boat trunk {i}{j}"] = {
                    "name": "Nothing",
                    "dest": None,
                    "pay": 0
                }

        self.money = STARTING_MONEY
        self.fuel = STARTING_FUEL


    def my_update(self, left_pressed, right_pressed, forward_pressed, backward_pressed):  
        derive = self.physique_body.velocity.dot(self.physique_body.rotation_vector.rotated_degrees(90))
        force = pymunk.Vec2d(0, -DERIVE_FORCE) * derive
        self.physics_engine.apply_force(self, force)
        #self.force = force.rotated(physique_body.angle)
        
        derive = self.physique_body.velocity_at_local_point((-10, 0)).dot(self.physique_body.rotation_vector.rotated_degrees(90 - self.barre / 10))
        force = pymunk.Vec2d(0, -DERIVE_FORCE) * derive
        self.physique_body.apply_force_at_local_point(force, (-10, 0))
        #self.force = force.rotated(physique_body.angle)

        if forward_pressed and self.fuel > 0:
            force = pymunk.Vec2d(ADV_FORCE, 0)
            self.physics_engine.apply_force(self, force)
            self.fuel -= 1/256
        if backward_pressed and self.fuel > 0:
            self.fuel -= 1/256
            force = pymunk.Vec2d(- ADV_FORCE, 0)
            self.physics_engine.apply_force(self, force)
        if right_pressed:
            self.barre = max(-MAX_BARRE, self.barre - BARRE_SPEED)
        if left_pressed:
            self.barre = min(MAX_BARRE, self.barre + BARRE_SPEED)


class BoatView(arcade.View):
    window: Window
    current: Optional[arcade.TiledObject] = None
    button: Optional[arcade.TiledObject] = None
    select_boat:  Optional[arcade.TiledObject] = None
    select_dock:  Optional[arcade.TiledObject] = None
    asset: dict
    market: dict
    boat_price: float = 0.0
    dock_price: float = 0.0

    def __init__(self, window: Window, boat: Boat, come_back):
        super().__init__(window)

        self.boat = boat
        self.come_back = come_back

        self.tile_map = arcade.load_tilemap("assets/boat.tmj", scaling=1)
        self.background = arcade.load_texture("assets/fond.png")

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list("Player")

        for img in self.tile_map.sprite_lists["Image"]:
            img.top = self.window.height

        for obj in self.tile_map.object_lists["coffres"]:
            for coord in obj.shape:
                coord[1] -= img.bottom + 48 # type: ignore[index]

        self.txt = []
        self.buttons = []

        for obj in self.tile_map.object_lists["boutons et texte"]:
            for coord in obj.shape:
                coord[1] -= img.bottom + 48 # type: ignore[index]

            if obj.type == "Button":
                self.buttons.append(obj)
                xs, ys = obj.shape[0]  # type: ignore[misc]
                xe, ye = obj.shape[2]  # type: ignore[misc]
                txt = arcade.Text(obj.properties["txt"], (xs + xe) / 2, (ys + ye) / 2, anchor_x="center", anchor_y="center") #type: ignore[index]
                self.txt.append(txt)  
            elif obj.name == "tobuy":
                self.tobuy = obj
            elif obj.name == "tosell":
                self.tosell = obj
            elif obj.name == "description":
                self.description = obj
            elif obj.name == "money":
                self.money = obj
            elif obj.name == "market":
                self.maket_zone = obj

    def default_select(self):
        for obj in self.tile_map.object_lists["coffres"]:
            if obj.type == "BoatTrunk" and self.boat.inventaire[obj.name]["name"] == "Nothing":
                self.select_boat = obj
                return

    def setup(self, dock, inventaire:dict, market:dict):
        self.dock = dock
        self.inventaire = inventaire
        self.market = market

        x, y = self.description.shape[0] #type: ignore[misc]
        width = int(self.description.shape[2][0] - x)  #type: ignore[index,misc]
        self.description_txt = arcade.Text(dock.properties["desc"], x, y, anchor_x="left", anchor_y="top", multiline=True, width=width)

        txt_lst = ["Buy price:"]
        for m, v in market.items():
            txt_lst.append(f"{m}: {v} $")

        txt = "\n  ".join(txt_lst)

        x, y = self.maket_zone.shape[0] #type: ignore[misc]
        width = int(self.maket_zone.shape[2][0] - x)  #type: ignore[index,misc]

        self.market_txt = arcade.Text(txt, x, y, anchor_x="left", anchor_y="top", multiline=True, width=width)

        self.default_select()

    def on_update(self, dt):
        self.selected_market_values()
    
    def selected_market_values(self):
        self.boat_price = 0.0
        self.dock_price = 0.0
        if self.select_boat:
            name = self.select_boat.name
            item = self.boat.inventaire[name]
            if item["name"] in self.market:
                self.boat_price = self.market[item["name"]]
            
        if self.select_dock:
            name = self.select_dock.name
            item = self.inventaire[name]
            if "value" in item:
                self.dock_price = item["value"]


    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.current = None
        for obj in self.tile_map.object_lists["coffres"]:
            if arcade.is_point_in_polygon(x, y, obj.shape):
                self.current = obj

        self.button = None
        for obj in self.buttons:
            if arcade.is_point_in_polygon(x, y, obj.shape):
                self.button = obj


        return super().on_mouse_motion(x, y, dx, dy)
    
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.come_back()
        return super().on_key_press(symbol, modifiers)


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.current:
            if self.current.type == "BoatTrunk":
                self.select_boat = self.current
            elif self.current.type == "PortTrunk":
                self.select_dock = self.current

        if self.button:
            if self.button.name == "exchange":
                self.exchange()
            elif self.button.name == "sell":
                self.sell()
            elif self.button.name == "leave":
                self.come_back()
        return super().on_mouse_press(x, y, button, modifiers)
    
    def exchange(self):
        if self.select_boat and self.select_dock and self.boat.money + self.boat_price - self.dock_price >= 0:
            self.boat.money += self.boat_price - self.dock_price
            dock_name = self.select_dock.name
            boat_name = self.select_boat.name
            self.inventaire[dock_name], self.boat.inventaire[boat_name] = self.boat.inventaire[boat_name], self.inventaire[dock_name]

            self.default_select()

    def sell(self):
        if self.select_boat:
            self.boat.money += self.boat_price
            self.boat.inventaire[self.select_boat.name] = { "name": "Nothing" }

    @staticmethod
    def draw_text_content(asset, pos, price_tag):
        x, y = pos
        arcade.draw_text(asset["name"], x, y, anchor_y="top")
        if "value" in asset:
            arcade.draw_text(f"{price_tag}: {asset['value']}", x, y - 40, anchor_y="top")

    def draw_money(self):
        x, y = self.money.shape[0]
        width = self.money.shape[2][0] - x

        txt = f"Cash: {self.boat.money}$"

        if self.boat_price != 0.0:
            txt += f",\nafter selling: {self.boat.money + self.boat_price}"

        if self.dock_price != 0.0:
            txt += f",\nafter exchange: {self.boat.money + self.boat_price - self.dock_price}"
        
        arcade.draw_text(txt, x, y, anchor_y="top", multiline=True, width=width)

    


    def on_draw(self):
        """ Draw everything """
        self.clear()

        self.scene.draw()

        for obj in self.tile_map.object_lists["coffres"]:
            arcade.draw_polygon_outline(obj.shape, RED)

        superior_asset = None
        inferior_asset = None

        if self.current:
            arcade.draw_polygon_filled(self.current.shape, RED)
            if self.current.type == "BoatTrunk":
                inferior_asset = self.boat.inventaire[self.current.name]
            elif self.current.type == "PortTrunk":
                superior_asset = self.inventaire[self.current.name]

        if self.select_dock:
            arcade.draw_polygon_filled(self.select_dock.shape, SELECTED)

            if superior_asset is None:
                superior_asset = self.inventaire[self.select_dock.name]


        if self.select_boat:
            arcade.draw_polygon_filled(self.select_boat.shape, SELECTED)

            if inferior_asset is None:
                inferior_asset = self.boat.inventaire[self.select_boat.name]

        width = self.tosell.shape[2][0] - self.tosell.shape[0][0]

        if superior_asset is not None:
            if "value" in superior_asset:
                txt = (f"Selected container\n"
                    f"    {superior_asset['name']}:"
                    f" for {superior_asset['value']} $")
            else:
                txt = "Selected container\n    Empty"
        else:
            txt = "No selected container in dock"
        arcade.draw_text(txt, self.tosell.shape[0][0], self.tosell.shape[0][1],
                             anchor_y="top",
                             multiline=True, width=width)

        if inferior_asset is not None:
            if "value" in inferior_asset:
                txt = (f"Selected container\n"
                    f"    {inferior_asset['name']}:"
                    f"\n    bought for {inferior_asset['value']} $")
            else:
                txt = "Selected container\n    Empty"
        else:
            txt = "No selected container in the boat"
        arcade.draw_text(txt, self.tobuy.shape[0][0], self.tobuy.shape[0][1],
                        anchor_y="top",
                        multiline=True, width=width)

        if self.button:
            arcade.draw_polygon_filled(self.button.shape, RED)

        for txt in self.txt:
            txt.draw()

        self.description_txt.draw()
        self.market_txt.draw()

        self.draw_money()

    def on_show_view(self):
        self.window.set_mouse_visible(True)
        return super().on_show_view()
    
    def on_hide_view(self):
        self.window.set_mouse_visible(False)
        return super().on_show_view()