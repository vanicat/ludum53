import arcade
import math
import pymunk

SCREEN_TITLE = "Ludum 32"

# Size of screen to show, in pixels
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 0.1
PLAYER_DAMPING = 0.1

# Friction between objects
PLAYER_FRICTION = 5
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

# Mass (defaults to 1)
PLAYER_MASS = 2.0

# Keep player from going too fast
PLAYER_MAX_SPEED = 450
ADV_FORCE = 300
ROTATE_FORCE = 150

class GameWindow(arcade.Window):
    """ Main Window """

    scene: arcade.Scene
    physics_engine: arcade.PymunkPhysicsEngine
    left_pressed: bool
    right_pressed: bool
    forward_pressed: bool
    backward_pressed: bool

    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)


    def setup(self):
        """ Set up everything with the game """
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING)

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True) 

        self.player_sprite = arcade.Sprite("assets/camion.png", 1)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 120
        self.scene.add_sprite("Player", self.player_sprite)
        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       collision_type="player",
                                       max_velocity=PLAYER_MAX_SPEED)
        


        self.left_pressed = False
        self.right_pressed =  False
        self.forward_pressed = False
        self.backward_pressed = False

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
        angle = self.player_sprite.radians
        if self.forward_pressed:
            print(angle)
            force = pymunk.Vec2d(ADV_FORCE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
        if self.backward_pressed:
            force = pymunk.Vec2d(- ADV_FORCE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
        if self.right_pressed:
            force = pymunk.Vec2d(ADV_FORCE, 0)
            apply = pymunk.Vec2d(0, 1)
            self.physics_engine.sprites[self.player_sprite].body.apply_force_at_local_point(force, apply)
            self.physics_engine.sprites[self.player_sprite].body.apply_force_at_local_point(-force, -apply)
        if self.left_pressed:
            force = pymunk.Vec2d(ADV_FORCE, 0)
            apply = pymunk.Vec2d(0, -1)
            self.physics_engine.sprites[self.player_sprite].body.apply_force_at_local_point(force, apply)
            self.physics_engine.sprites[self.player_sprite].body.apply_force_at_local_point(-force, -apply)

        self.physics_engine.step()

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.scene.draw()
        angle = self.player_sprite.radians
        force = pymunk.Vec2d(ADV_FORCE, 0).rotated(angle)
        x = self.player_sprite.center_x
        y = self.player_sprite.center_y
        arcade.draw_line(x, y, x + force.x, y + force.y, (200, 0, 100))



def main():
    """ Main function """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()