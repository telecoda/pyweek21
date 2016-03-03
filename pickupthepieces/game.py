import os, pygame, random
from pygame.locals import *
from data import load
from piece import Piece

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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
        self.background_image = load_image('background.png')
        self.title_image = load_image('title.png')
        self.shadow_image = load_image('shadow.png')

        self.font_16 = load_font('ApocalypseDeluxe-Regular.ttf', 16)
        self.font_24 = load_font('ApocalypseDeluxe-Regular.ttf', 24)
        self.font_36 = load_font('ApocalypseDeluxe-Regular.ttf', 36)


    def render(self):
        # self.screen.fill((0, 0, 0))
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

        self.render_shadow_text(
            self.font_24, "Playing", self.cx, 50, (255, 255, 0), -2, CENTRE)


    def render_menu(self):
        self.screen.blit(self.title_image, (0, 0))
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
            elif self.state == PAUSED:
                quit = self.handle_paused_events()
            elif self.state == GAME_OVER:
                quit = self.handle_game_over_events()

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
            print "Completed!"

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

    def start_game(self):
        self.state = PLAYING
        self.level = 1
        self.start_level()

    def start_level(self):
        # init puzzle images
        self.current_image =self.level_images[self.level]
        self.max_dist = 500
        self.max_angle = 50
        self.rows = 4
        self.cols = 4
        self.pieces = self.split_image(self.current_image,self.rows,self.cols)
        self.current_piece = None
        self.puzzle_width = self.current_image.get_width()
        self.puzzle_height = self.current_image.get_height()
        self.piece_width = self.puzzle_width / self.rows
        self.piece_height = self.puzzle_height / self.cols
        self.puzzle_complete = False
        self.shuffle_pieces(max_angle=self.max_angle, max_dist=self.max_dist)
        self.pieces_to_place = len(self.pieces)

    def shuffle_pieces(self, max_dist=100, max_angle=0):
        for piece in self.pieces:
            # random angle
            new_angle = random.randint(0,max_angle) / 5 * 5
            new_x_offset = random.randint(0,max_dist) + piece.x_offset
            new_y_offset = random.randint(0,max_dist) + piece.y_offset
            piece.move((new_x_offset, new_y_offset), new_angle)

        # scale puzzle to fit all pieces on screen
        self.scale_puzzle(max_dist)

    def scale_puzzle(self,max_dist):
        """
        Scale size of piece so they all fit on screen
        """
        # min_x = self.screen.get_width()/2
        # min_y = self.screen.get_height()/2
        # max_x = min_x
        # max_y = min_y
        # for piece in self.pieces:
        #     # calc min/max values
        #     if piece.width > piece.height:
        #         piece_size = piece.width
        #     else:
        #         piece_size = piece.height
            
        #     max_piece_x = piece.x_offset +(2 * piece_size)
        #     min_piece_x = piece.x_offset
        #     max_piece_y = piece.y_offset + (2 * piece_size)
        #     min_piece_y = piece.y_offset

        #     if min_piece_x < min_x:
        #         min_x = min_piece_x
        #     if min_piece_y < min_y:
        #         min_y = min_piece_y
        #     if max_piece_x > max_x:
        #         max_x = max_piece_x
        #     if max_piece_y > max_y:
        #         max_y = max_piece_y

        # # calc total size required
        # width = max_x - min_x
        # height = max_y - min_y

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