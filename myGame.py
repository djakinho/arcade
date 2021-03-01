"""
My "another attempt to make a game"...
Let's do this!

Better Move Sprite With Keyboard
"""

import arcade
import os
from time import *
import threading

SPRITE_SCALING = 0.5
BOMB_SCALING = 0.05

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Tha Game"

MOVEMENT_SPEED = 5


class Bomb(arcade.Sprite):
    pass


class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where to find files)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # This variable holds our simple "physics engine"
        self.physics_engine = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.brick_list = None
        self.bomb_list = None


        # Set up the player info
        self.player_sprite = None


        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.brick_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("character_femalePerson_idle.png", SPRITE_SCALING-0.125)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Set up the bricks
        # Place bricks inside a loop
        for x in range(64, SCREEN_WIDTH -1, 128):
            for y in range(128, SCREEN_HEIGHT -1, 128):                 # Need to fix.
                wall = arcade.Sprite("brickGrey.png", SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                self.brick_list.append(wall)

        # Set up our simple "physics engine"
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.brick_list)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.brick_list.draw()
        self.bomb_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Explode the Bomb
        # Set a counter


        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # Call update to move the sprite
        # If using a physics engine, call update on it stead of the sprite list
        # self.player_list.update()                     # Fix why window "collision" isn't working
        self.physics_engine.update()
        self.bomb_list.update()

    # def countdown(self, thebomb):
    #     global my_timer
    #     my_timer = 5
    #
    #     for x in range(5):
    #         my_timer -= my_timer
    #         sleep(1)
    #
    #     print('bum')
    #     thebomb.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """

        if key == arcade.key.Z:
            # global bomb
            bomb = Bomb("blackberry.png", BOMB_SCALING)
            bomb.center_x = self.player_sprite.center_x
            bomb.center_y = self.player_sprite.center_y
            self.bomb_list.append(bomb)

            # countdown_thread = threading.Thread(target=MyGame.countdown, args=[self, bomb])
            # countdown_thread.start()

            print(len(self.bomb_list))



        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """ Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


def main():
    """ Main Method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()