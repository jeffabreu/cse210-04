import random
from game.casting.player import Player
from game.shared.color import Color
from game.shared.point import Point
from game.casting.gem import Gem

COLS = 60
ROWS = 40
DEFAULT_GEMS = 40

class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.
    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service

    def start_game(self, cast, player):
        """Starts the game using the given cast. Runs the main game loop.
        Args:
            cast (Cast): The cast of actors.
        """
        self._CELL_SIZE = 15
        self._FONT_SIZE = 15
        self._video_service.open_window()
        self.create_gems(cast)
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast, player)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)        

    def _do_updates(self, cast, player):
        """Updates the robot's position and resolves any collisions with gems.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        gems = cast.get_actors("gems")

        banner.set_text("Your Score: " + player.get_score())
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)
        
        for gem in gems:
            # move gems down a block
            gem.move_next(max_x, max_y)
            # if robot has hit a gem
            if robot.get_position().equals(gem.get_position()):
                # if a gem has been caught, increase trhe players score by the gem points and increase the score of the next gem generated
                if gem.get_text() == "*":
                    player.set_score(gem.get_score())
                    gem.increase_score()
                    score = gem.get_score()
                else:
                    # If it is a O reduce player score by 1
                    score = -1
                    player.set_score(-1)
                
                # Update the banner, create a new gem and remove the found gem
                banner.set_text(player.get_score()) 
                self.create_gem(cast, score)   
                cast.remove_actor("gems", gem)
        
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()

    def create_gems(self, cast):
         # create the initial gems and squares
        for n in range(DEFAULT_GEMS):
            text = '*' if random.randint(1,2) == 1 else 'O'
            gem = self.assign_gem_values(cast, 1 if text == '*' else -1, text)
            gem.set_score(1 if text == '*' else -1)
            cast.add_actor("gems", gem)

    def create_gem(self, cast, score):
        # create an individual gem
        text = '*' if random.randint(1,2) == 1 else 'O'
        gem = self.assign_gem_values(cast, 1 if text == '*' else -1, text)
        gem.set_score(score)
        cast.add_actor("gems", gem)


    def assign_gem_values(self, cast, score, text):
        x = random.randint(1, COLS - 1)
        y = random.randint(1, ROWS - 1)
        position = Point(x, y)
        position = position.scale(self._CELL_SIZE)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = Color(r, g, b)
        
        gem = Gem()
        gem.set_text(text)
        gem.set_font_size(self._FONT_SIZE)
        gem.set_velocity(Point(0,3))
        gem.set_color(color)
        gem.set_position(position)
        gem.set_score(score)
        cast.add_actor("gems", gem)

        return gem
