import pymunk
import arcade

from const import *

class Boat(arcade.Sprite):
    camera: arcade.Camera
    physics_engine: arcade.PymunkPhysicsEngine
    physique_body: pymunk.Body
    barre: float

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
