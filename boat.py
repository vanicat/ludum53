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

    def __init__(self, pos:tuple[float, float], scene:arcade.Scene, engine:arcade.PymunkPhysicsEngine):
        super().__init__("assets/boat.png", 1)
        self.center_x = pos[0]
        self.center_y = pos[1]
        scene.add_sprite("Player", self)
        self.physics_engine = engine

        self.physics_engine.add_sprite(self,
                               friction=PLAYER_FRICTION,
                               mass=PLAYER_MASS,
                               collision_type="player",
                               max_velocity=PLAYER_MAX_SPEED)
        body = self.physics_engine.sprites[self].body
        assert body is not None
        self.physique_body = body

        self.barre = 0

        self.inventaire = {}
        for i in range(4):
            for j in range(3):
                self.inventaire[f"boat trunk {i}{j}"] = f"empty {3*i+j} \n\n capacity : 1000"


    def my_update(self, left_pressed, right_pressed, forward_pressed, backward_pressed):  
        derive = self.physique_body.velocity.dot(self.physique_body.rotation_vector.rotated_degrees(90))
        force = pymunk.Vec2d(0, -DERIVE_FORCE) * derive
        self.physics_engine.apply_force(self, force)
        #self.force = force.rotated(physique_body.angle)
        
        derive = self.physique_body.velocity_at_local_point((-10, 0)).dot(self.physique_body.rotation_vector.rotated_degrees(90 - self.barre / 10))
        force = pymunk.Vec2d(0, -DERIVE_FORCE) * derive
        self.physique_body.apply_force_at_local_point(force, (-10, 0))
        #self.force = force.rotated(physique_body.angle)

        if forward_pressed:
            force = pymunk.Vec2d(ADV_FORCE, 0)
            self.physics_engine.apply_force(self, force)
        if backward_pressed:
            force = pymunk.Vec2d(- ADV_FORCE, 0)
            self.physics_engine.apply_force(self, force)
        if right_pressed:
            self.barre = max(-MAX_BARRE, self.barre - BARRE_SPEED)
        if left_pressed:
            self.barre = min(MAX_BARRE, self.barre + BARRE_SPEED)


class BoatView(arcade.View):
    window: Window
    current: Optional[arcade.TiledObject] = None
    select_boat:  Optional[arcade.TiledObject] = None
    select_dock:  Optional[arcade.TiledObject] = None

    def __init__(self, window: Window, boat: Boat, come_back):
        super().__init__(window)

        self.boat = boat
        self.come_back = come_back

        self.tile_map = arcade.load_tilemap("assets/boat.tmx", scaling=1)
        self.background = arcade.load_texture("assets/fond.png")

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list("Player")

        for img in self.tile_map.sprite_lists["Image"]:
            img.top = self.window.height

        for obj in self.tile_map.object_lists["coffres"]:
            for coord in obj.shape:
                coord[1] += self.window.height # type: ignore[index]

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.current = None
        for obj in self.tile_map.object_lists["coffres"]:
            if arcade.is_point_in_polygon(x, y, obj.shape):
                self.current = obj
        return super().on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.come_back()
        return super().on_key_press(symbol, modifiers)
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.current:
            if self.current.type == "BoatTrunk":
                self.select_boat = self.current
            else:
                self.select_dock = self.current
        return super().on_mouse_press(x, y, button, modifiers)

    def on_draw(self):
        """ Draw everything """
        self.clear()

        self.scene.draw()

        for obj in self.tile_map.object_lists["coffres"]:
            arcade.draw_polygon_outline(obj.shape, RED)

        if self.current:
            arcade.draw_polygon_filled(self.current.shape, RED)
            if self.current.type == "BoatTrunk":
                arcade.draw_text(self.boat.inventaire[self.current.name], 765 + 30, self.window.height / 2 - 30)

        if self.select_dock:
            arcade.draw_polygon_filled(self.select_dock.shape, SELECTED)

        if self.select_boat:
            arcade.draw_polygon_filled(self.select_boat.shape, SELECTED)

            if self.current is None or self.current.type != "BoatTrunk":
                arcade.draw_text(self.boat.inventaire[self.select_boat.name], 765 + 30, self.window.height / 2 - 30)


    def on_show_view(self):
        self.window.set_mouse_visible(True)
        return super().on_show_view()
    
    def on_hide_view(self):
        self.window.set_mouse_visible(False)
        return super().on_show_view()