import os, pygame, random, time
from pygame.locals import *
from data import load, filepath
from piece import Piece
from levels import levels

mixer = pygame.mixer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

KEY_REPEAT = 50  # Key repeat in milliseconds

# Game states
MENU = 0
INSTRUCTIONS = 1
LEVEL_INTRO = 2
PLAYING = 3
LEVEL_COMPLETED = 4
PAUSED = 5
GAME_OVER = 6
GAME_COMPLETED = 7

# Alignment
CENTRE = 0
LEFT = 1
RIGHT = 2
TOP = 3
MIDDLE = 4
BOTTOM = 5

# COLOURS
MENU_WHITE = (255,255,255)
MENU_BROWN = (109,69,27)
MENU_YELLOW = (255,255,0)
MENU_GREY = (160,160,160)
TIMER = (255, 255, 255)
TIMER_SIREN = (255, 0, 0)
SCORE_COLOUR = (255, 255, 255)

def load_sound(file):
    "loads a sound"
    try:
         sound = mixer.Sound(filepath(file))
    except pygame.error:
        raise SystemExit('Could not load sound "%s" %s' %
                         (file, pygame.get_error()))
    return sound

def load_music(file):
    "loads music"
    try:
         music = mixer.music.load(filepath(file))
    except pygame.error:
        raise SystemExit('Could not load music "%s" %s' %
                         (file, pygame.get_error()))
    return music


def load_image(file):
    "loads an image"
    file = load(file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    return surface.convert_alpha()


def load_font(file, size):
    "loads a font"
    file = load(file)
    try:
        font = pygame.font.Font(file, size)
    except pygame.error:
        raise SystemExit('Could not load font "%s" %s' %
                         (file, pygame.get_error()))
    return font


class PickUpPieces(object):

    def __init__(self):

        # Initialize Everything
        pygame.init()

        mixer.init(44100)

        pygame.display.set_caption("Pick up the pieces")
        pygame.key.set_repeat(KEY_REPEAT)

        flags = DOUBLEBUF | HWSURFACE
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), flags)

        self.cx = SCREEN_WIDTH/2
        self.cy = SCREEN_HEIGHT/2

        self.levels = levels
        self.max_levels = len(levels)-1

        self.init_assets()
        self.clock = pygame.time.Clock()
        self.current_music = None
        self.reset_game()

    def reset_game(self):
        self.state = MENU
        if self.current_music:
            self.current_music.stop()
        self.current_music = self.intro_music
        self.current_music.play(-1)
        self.current_piece = None
        self.current_level = 1
        self.score = 0
        self.scale = 1.0
        self.pos_cx = 0.0
        self.pos_cy = 0.0

    def handle_playing_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == MOUSEBUTTONDOWN:
                self.start_dragging_piece(mouse_pos)
            elif event.type == MOUSEBUTTONUP:
                self.stop_dragging_piece(mouse_pos)
            elif event.type == MOUSEMOTION:
                self.drag_piece(mouse_pos)
            elif event.type == KEYDOWN and (event.key == K_a or event.key == K_LEFT):
                self.rotate_piece_left()
            elif event.type == KEYDOWN and (event.key == K_d or event.key == K_RIGHT):
                self.rotate_piece_right()
            # TEMP: level skip
            # elif event.type == KEYDOWN and event.key == K_SPACE:
            #     self.level_completed()


    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == MOUSEBUTTONDOWN:
                self.show_instructions()

    def handle_instructions_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == MOUSEBUTTONDOWN:
                self.start_level_intro()

    def handle_level_intro_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == MOUSEBUTTONDOWN:
                self.start_level()

    def handle_level_completed_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == MOUSEBUTTONDOWN:
                self.start_next_level()


    def handle_paused_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True


    def handle_game_over_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == MOUSEBUTTONDOWN:
                self.reset_game()

    def handle_game_completed_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == MOUSEBUTTONDOWN:
                self.reset_game()


    def init_assets(self):
        self.background_image = load_image('background.png')
        self.title_image = load_image('title.png')
        self.shadow_image = load_image('shadow.png')
        self.ending_image = load_image('ending.png')
        self.game_over_image = load_image('game-over.jpg')

        self.font_16 = load_font('ApocalypseDeluxe-Regular.ttf', 16)
        self.font_24 = load_font('ApocalypseDeluxe-Regular.ttf', 24)
        self.font_36 = load_font('ApocalypseDeluxe-Regular.ttf', 36)
        self.font_48 = load_font('ApocalypseDeluxe-Regular.ttf', 48)
        self.font_72 = load_font('ApocalypseDeluxe-Regular.ttf', 72)

        self.paper_sound = load_sound('paper-flip.wav')
        self.siren_sound = load_sound('siren.wav')
        self.ticking_sound = load_sound('ticking.wav')
        self.intro_music = load_sound('intro.wav')
        self.ending_music = load_sound('ending.wav')
        self.bombs_sound = load_sound('bombs-dropping.wav')


    def render(self):
        # self.screen.fill((0, 0, 0))
        if self.state == PLAYING:
            self.render_playing()
        elif self.state == PAUSED:
            self.render_paused()
        elif self.state == GAME_OVER:
            self.render_game_over()
        elif self.state == INSTRUCTIONS:
            self.render_instructions()
        elif self.state == LEVEL_INTRO:
            self.render_level_intro()
        elif self.state == LEVEL_COMPLETED:
            self.render_level_completed()
        elif self.state == GAME_COMPLETED:
            self.render_game_completed()
        else:
            self.render_menu()

        self.clock.tick()

        #self.render_fps()
        pygame.display.flip()

    def render_playing(self):

        # render level image
        # self.screen.blit(
        #     self.level_images[1], (0, 0))
        self.screen.blit(self.background_image, (0, 0))
        for piece in self.pieces:
            piece.render_position(self.screen) 

        # render placed puzzle pieces
        for piece in self.pieces:
            if piece.in_position:
                piece.render(self.screen) 

        # render unplaced puzzle pieces
        for piece in self.pieces:
            if not piece.in_position:
                piece.render(self.screen) 

        self.render_score()
        self.render_time()

    def render_score(self):
        # score
        score_str = "Score: %d" % self.score 
        self.render_shadow_text(
            self.font_24, score_str, 5, 5, SCORE_COLOUR, -2, LEFT)

    def render_time(self):
        # time
        self.time_remaining = self.end_time - time.time()
        secs = self.time_remaining % 60
        mins = self.time_remaining / 60
        time_str = "Time: %d:%02d" % (mins,secs) 

        if self.time_remaining < 0:
            self.game_over()

        if self.time_remaining < 41 and not self.siren_started:
            self.siren_sound.play()
            self.siren_started = True

        colour = TIMER
        if self.siren_started:
            colour = TIMER_SIREN
        self.render_shadow_text(
            self.font_24, time_str, self.screen.get_width()-5, 5, colour, -2, RIGHT)

    def render_instructions(self):
        self.screen.blit(self.title_image, (0, 0))
        self.render_shadow_text(
            self.font_72, "Instructions", self.cx, 0, MENU_WHITE, -2, CENTRE)

        text_y = 100
        for text in self.levels[0].get("text"):
            self.render_shadow_text(
                self.font_24, text, self.cx, text_y, MENU_YELLOW, -2, CENTRE)
            text_y += 30

        self.render_shadow_text(
            self.font_72, "Click to continue", self.cx, 500, MENU_GREY, -2, CENTRE)

    def render_level_intro(self):
        self.screen.blit(self.title_image, (0, 0))
        self.render_shadow_text(
            self.font_72, self.level.get("name"), self.cx, 0, MENU_WHITE, -2, CENTRE)
        
        text_y = 100
        for text in self.level.get("text"):
            self.render_shadow_text(
                self.font_24, text, self.cx, text_y, MENU_WHITE, -2, CENTRE)
            text_y += 30

        self.render_shadow_text(
            self.font_72, "Click to continue", self.cx, 500, MENU_GREY, -2, CENTRE)

    def render_level_completed(self):
        self.screen.blit(self.background_image, (0, 0))
        x_offset = (self.screen.get_width() - self.current_image.get_width())/2
        y_offset = (self.screen.get_height() - self.current_image.get_height())/2
        self.screen.blit(self.current_image, (x_offset, y_offset))
        self.render_shadow_text(
            self.font_72, "Level complete", self.cx, 0, MENU_WHITE, -2, CENTRE)
        self.render_shadow_text(
            self.font_72, "Click to continue", self.cx, self.cy, MENU_GREY, -2, CENTRE)

    def render_game_completed(self):
        self.screen.blit(self.background_image, (0, 0))
        x_offset = (self.screen.get_width() - self.current_image.get_width())/2
        y_offset = (self.screen.get_height() - self.current_image.get_height())/2
        self.screen.blit(self.ending_image, (x_offset, 80))
        self.render_shadow_text(
            self.font_72, "Congratulations!", self.cx, 0, MENU_WHITE, -2, CENTRE)
        self.render_shadow_text(
            self.font_72, "Click to continue", self.cx, self.cy, MENU_GREY, -2, CENTRE)

    def render_menu(self):
        self.screen.blit(self.title_image, (0, 0))
        self.render_shadow_text(
            self.font_72, "Picking up the pieces", self.cx, 0, MENU_WHITE, -2, CENTRE)
        self.render_shadow_text(

            self.font_16, "by Telecoda", 700, 70, MENU_WHITE, -2, RIGHT)
        self.render_shadow_text(
            self.font_72, "Click to start", self.cx, self.cy, MENU_GREY, -2, CENTRE)


    def render_fps(self):
        fps = 'fps:%f' % self.clock.get_fps()
        self.render_shadow_text(
            self.font_16, fps, 0, 0, (255, 255, 255), -2, LEFT)



    def render_paused(self):
        pass

    def render_game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))
        x_offset = (self.screen.get_width() - self.current_image.get_width())/2
        y_offset = (self.screen.get_height() - self.current_image.get_height())/2
        self.render_shadow_text(
            self.font_72, "Game over", self.cx, 0, MENU_WHITE, -2, CENTRE)
        self.render_shadow_text(
            self.font_72, "Click to continue", self.cx, self.cy, MENU_GREY, -2, CENTRE)
        self.render_score()

    def render_shadow_text(self, font, text, x, y, colour, shadow_offset=-2, align=CENTRE):
        surface = font.render(text, 1, (0,0,0))

        # default to top left , no offset
        x_offset = 0
        y_offset = 0

        if align == CENTRE:
        # calc x offset
            x_offset = - surface.get_width() / 2
        elif align == LEFT:
            x_offset = 0
        elif align == RIGHT:
            x_offset = - surface.get_width()

        self.screen.blit(surface, (x + x_offset, y + y_offset))

        surface = font.render(text, 1, (colour))
        self.screen.blit(
            surface, (x + x_offset + shadow_offset, y + y_offset + shadow_offset))

    def rotate_piece_left(self):
        if self.current_piece:
            placed = self.current_piece.rotate_left()
            if placed:
                self.piece_placed()

    def rotate_piece_right(self):
        if self.current_piece:
            placed = self.current_piece.rotate_right()
            if placed:
                self.piece_placed()


    def run(self):
        quit = False

        while not quit:
            # Handle Input Events
            if self.state == PLAYING:
                quit = self.handle_playing_events()
            elif self.state == MENU:
                quit = self.handle_menu_events()
            elif self.state == INSTRUCTIONS:
                quit = self.handle_instructions_events()
            elif self.state == PAUSED:
                quit = self.handle_paused_events()
            elif self.state == GAME_OVER:
                quit = self.handle_game_over_events()
            elif self.state == LEVEL_INTRO:
                quit = self.handle_level_intro_events()
            elif self.state == LEVEL_COMPLETED:
                quit = self.handle_level_completed_events()
            elif self.state == GAME_COMPLETED:
                quit = self.handle_game_completed_events()

            self.render()

    def start_dragging_piece(self, mouse_pos):
        # check if polygon is click on
        for piece in reversed(self.pieces):
            if not piece.in_position:
                if piece.rotated_polygon.collidepoint(mouse_pos):
                    self.current_piece = piece
                    self.last_drag_pos = mouse_pos
                    self.current_piece.start_dragging()
                    break

    def drag_piece(self, mouse_pos):
        if self.current_piece:
            # move diff
            x_delta = mouse_pos[0]-self.last_drag_pos[0]
            y_delta = mouse_pos[1]-self.last_drag_pos[1]
            self.last_drag_pos = mouse_pos
            placed = self.current_piece.drag((x_delta,y_delta))
            if placed:
                self.piece_placed()

    def piece_placed(self):
        self.pieces_to_place -= 1
        if self.pieces_to_place == 0:
            self.level_completed()

    def stop_dragging_piece(self, mouse_pos):
        if self.current_piece:
            self.current_piece.stop_dragging()
            self.current_piece = None

        # removed dynamic scaling, too complex given the time constraints
        #self.scale_puzzle()


    def split_image(self, whole_image, rows, cols):
        """
        Splits a single image into separate image
        by rows and cols
        """
        piece_width = whole_image.get_width()/rows
        piece_height = whole_image.get_height()/cols

        pieces = []

        for col in range(0,cols):
            for row in range(0,rows):

                start_x = row * piece_width
                start_y = col * piece_height
                rect = pygame.Rect(start_x,start_y,piece_width,piece_height)

                image_piece = whole_image.subsurface(rect)
                # create matching shadow image
                shadow_image = pygame.transform.smoothscale(self.shadow_image,(piece_width, piece_height))
                piece = Piece(self, row,col,image_piece, shadow_image,start_x - piece_width / 2,start_y - piece_height / 2)

                pieces.append(piece)

        return pieces

    def show_instructions(self):
        self.state = INSTRUCTIONS

    def start_level_intro(self):
        self.state = LEVEL_INTRO
        self.level = self.levels[self.current_level]

    # def start_game(self):
    #     self.state = PLAYING
    #     self.start_level()

    def start_level(self):
        # init puzzle images
        if self.current_music:
            self.current_music.stop()
            self.siren_sound.stop()

        self.current_image =load_image(self.level.get('image_name'))
        self.current_music =load_sound(self.level.get('music'))
        self.rows = self.level.get("rows",2)
        self.cols = self.level.get("cols",2)
        self.max_dist = self.level.get("max_dist",100)
        self.max_angle = self.level.get("max_angle",0)
        self.time_limit = self.level.get('time_limit',99)
        self.start_time = time.time()
        self.end_time = self.start_time + self.time_limit
        self.pieces = self.split_image(self.current_image,self.rows,self.cols)
        self.current_piece = None
        self.puzzle_width = self.current_image.get_width()
        self.puzzle_height = self.current_image.get_height()
        self.piece_width = self.puzzle_width / self.rows
        self.piece_height = self.puzzle_height / self.cols
        self.puzzle_complete = False
        self.shuffle_pieces(max_angle=self.max_angle, max_dist=self.max_dist)
        self.pieces_to_place = len(self.pieces)
        self.state = PLAYING
        #self.ticking_sound.play(-1)
        self.siren_started = False
        self.current_music.play()

    def level_completed(self):
        self.state = LEVEL_COMPLETED
        self.score += self.time_remaining
        #self.ticking_sound.stop()
        #self.current_music.stop()

    def game_completed(self):
        self.state = GAME_COMPLETED
        if self.current_music:
            self.current_music.stop()
        self.current_music = self.ending_music

        #self.ticking_sound.stop()
        self.current_music.play()

    def game_over(self):
        self.state = GAME_OVER
        if self.current_music:
            self.current_music.stop()
        self.bombs_sound.play()


    def start_next_level(self):
        self.current_level += 1
        if self.current_level > self.max_levels:
            self.game_completed()
        else:
            self.start_level_intro()

    def shuffle_pieces(self, max_dist=100, max_angle=0):
        
        # swap piece offset

        offsets = []
        for piece in self.pieces:
            # random angle
            offset = (piece.x_offset, piece.y_offset)
            offsets.append(offset)

        # update piece with random offset
        for piece in self.pieces:
            i = random.randint(0,len(offsets)-1)
            new_offset = offsets[i]
            del offsets[i]
            piece.x_offset = new_offset[0]
            piece.y_offset = new_offset[1]

        for piece in self.pieces:
            # random angle
            new_angle = random.randint(0,max_angle) / 5 * 5
            new_x_offset = random.randint(0,max_dist)
            new_y_offset = random.randint(0,max_dist/2)



            piece.move((new_x_offset, new_y_offset), new_angle)

        # scale puzzle to fit all pieces on screen
        self.scale_puzzle(max_dist)

    def scale_puzzle(self,max_dist):
        """
        Scale size of piece so they all fit on screen
        """
        width = self.screen.get_width() + max_dist * 2
        height = self.screen.get_height() + max_dist * 2
        x_scale = float(self.screen.get_width()) / float(width)
        y_scale = float(self.screen.get_height()) / float(height)

        # pick max dimension to scal by
        if x_scale > y_scale:
            self.scale = x_scale
        else:
            self.scale = y_scale

        self.pos_cx = (width - self.puzzle_width) /2
        self.pos_cy = (height - self.puzzle_height) /2 - max_dist / 2 

        # print "min_x: %d max_x: %d min_y: %d max_y: %d" % (min_x, max_x, min_x, max_y)