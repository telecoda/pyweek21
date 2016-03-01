import os, pygame, random
from pygame.locals import *
from data import load
from piece import Piece

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

KEY_REPEAT = 50  # Key repeat in milliseconds

# Game states
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3

# Alignment
CENTRE = 0
LEFT = 1
RIGHT = 2
TOP = 3
MIDDLE = 4
BOTTOM = 5

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

        pygame.display.set_caption("Pick up the pieces")
        pygame.key.set_repeat(KEY_REPEAT)

        flags = DOUBLEBUF | HWSURFACE
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), flags)

        self.cx = SCREEN_WIDTH/2
        self.cy = SCREEN_HEIGHT/2

        self.init_assets()
        self.clock = pygame.time.Clock()
        self.state = MENU
        self.current_piece = None

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
            elif event.type == KEYDOWN and event.key == K_a:
                self.rotate_piece_left()
            elif event.type == KEYDOWN and event.key == K_d:
                self.rotate_piece_right()


    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == MOUSEBUTTONDOWN:
                self.start_game()

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


    def init_assets(self):
        self.level_images = {}
        self.level_images[1] = load_image('level-1.jpg')

        self.font_16 = load_font('space age.ttf', 16)
        self.font_24 = load_font('space age.ttf', 24)
        self.font_36 = load_font('space age.ttf', 36)


    def render(self):
        self.screen.fill((0, 0, 0))
        if self.state == PLAYING:
            self.render_playing()
        elif self.state == PAUSED:
            self.render_paused()
        elif self.state == GAME_OVER:
            self.render_game_over()
        else:
            self.render_menu()

        self.clock.tick()

        self.render_fps()
        pygame.display.flip()

    def render_playing(self):

        # render level image
        # self.screen.blit(
        #     self.level_images[1], (0, 0))

        # render puzzle pieces
        for piece in self.pieces:
            piece.render(self.screen) 
            #piece.angle += 1.0

        #self.pieces[0].render(self.screen)
        #self.pieces[0].angle += 1.0
        self.render_shadow_text(
            self.font_24, "Playing", self.cx, 50, (255, 255, 0), -2, CENTRE)


    def render_menu(self):
        self.render_shadow_text(
            self.font_24, "Pick up the pieces", self.cx, 0, (255, 0, 0), -2, CENTRE)
        self.render_shadow_text(
            self.font_24, "Click to start", self.cx, 50, (255, 255, 0), -2, CENTRE)

    def render_fps(self):
        fps = 'fps:%f' % self.clock.get_fps()
        self.render_shadow_text(
            self.font_16, fps, 0, 0, (255, 255, 255), -2, LEFT)



    def render_paused(self):
        pass

    def render_game_over(self):
        pass

    def render_shadow_text(self, font, text, x, y, colour, shadow_offset=-2, align=CENTRE):
        surface = font.render(text, 1, colour)

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

        # surface = font.render(text, 1, colour)
        # surface = self.scale_image(surface)
        # self.screen.blit(

    def rotate_piece_left(self):
        if self.current_piece:
            self.current_piece.rotate_left()

    def rotate_piece_right(self):
        if self.current_piece:
            self.current_piece.rotate_right()

    def run(self):
        quit = False

        while not quit:
            # Handle Input Events
            if self.state == PLAYING:
                quit = self.handle_playing_events()
            elif self.state == MENU:
                quit = self.handle_menu_events()
            elif self.state == PAUSED:
                quit = self.handle_paused_events()
            elif self.state == GAME_OVER:
                quit = self.handle_game_over_events()

            self.render()

    def start_dragging_piece(self, mouse_pos):
        # check if polygon is click on
        for piece in reversed(self.pieces):
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
            self.current_piece.drag((x_delta,y_delta))

            self.last_drag_pos = mouse_pos


    def stop_dragging_piece(self, mouse_pos):
        if self.current_piece:
            self.current_piece.stop_dragging()
            self.current_piece = None


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
                piece = Piece(row,col,image_piece,start_x - piece_width / 2,start_y - piece_height / 2)

                pieces.append(piece)

        return pieces

    def start_game(self):
        self.state = PLAYING
        self.level = 1
        self.start_level()

    def start_level(self):
        # init puzzle images
        self.pieces = self.split_image(self.level_images[self.level],3,3)
        self.current_piece = None
        self.puzzle_complete = False
        self.shuffle_pieces()

    def shuffle_pieces(self):
        for piece in self.pieces:
            # random angle
            new_angle = random.randint(0,360) / 5 * 5
            new_x_offset = random.randint(0,200)
            new_y_offset = random.randint(0,200)
            piece.move((new_x_offset, new_y_offset), new_angle)
