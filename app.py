import arcade
import math
import pymunk

SCREEN_TITLE = "Ludum 32"

# Size of screen to show, in pixels
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 0.7
PLAYER_DAMPING = DEFAULT_DAMPING

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
DERIVE_FORCE = 10

BARRE_SPEED = 2.5

class GameWindow(arcade.Window):
    """ Main Window """

    scene: arcade.Scene
    physics_engine: arcade.PymunkPhysicsEngine
    left_pressed: bool
    right_pressed: bool
    forward_pressed: bool
    backward_pressed: bool
    barre: float
    camera: arcade.Camera
    gui_camera: arcade.Camera

    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)


    def setup(self):
        """ Set up everything with the game """
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING)

        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        self.gui = arcade.Scene()
        self.gui.add_sprite_list("GUI")
        self.roue = arcade.Sprite("assets\la roue.png", 4) 
        self.roue.center_x = self.width - 64
        self.roue.center_y = self.height - 64
        self.gui.add_sprite("GUI", self.roue)

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True) 

        self.player_sprite = arcade.Sprite("assets/boat.png", 1)
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
        self.force = None
        self.barre = 0.0
        

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
        physique_body = self.physics_engine.sprites[self.player_sprite].body
        
        derive = physique_body.velocity.dot(physique_body.rotation_vector.rotated_degrees(90))
        force = pymunk.Vec2d(0, -DERIVE_FORCE) * derive
        self.physics_engine.apply_force(self.player_sprite, force)
        #self.force = force.rotated(physique_body.angle)
        
        derive = physique_body.velocity_at_local_point((-10, 0)).dot(physique_body.rotation_vector.rotated_degrees(90 - self.barre / 10))
        force = pymunk.Vec2d(0, -DERIVE_FORCE) * derive
        physique_body.apply_force_at_local_point(force, (-10, 0))
        #self.force = force.rotated(physique_body.angle)

        if self.forward_pressed:
            force = pymunk.Vec2d(ADV_FORCE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
        if self.backward_pressed:
            force = pymunk.Vec2d(- ADV_FORCE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
        if self.right_pressed:
            self.barre -= BARRE_SPEED
        if self.left_pressed:
            self.barre += BARRE_SPEED

        self.physics_engine.step()

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.camera.move_to((self.player_sprite.center_x - self.camera.viewport_width / 2, 
                             self.player_sprite.center_y - self.camera.viewport_height / 2), .5)
        self.camera.use()
        self.scene.draw()

        self.roue.angle = self.barre

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