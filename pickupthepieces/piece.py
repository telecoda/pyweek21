import pygame
import math
from pylygon import Polygon

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
GREY =   (128, 128, 128)

CENTRE_CROSS_SIZE = 10

ROTATION_SPEED = 5

LOCATION_ACCURACY = 10
ANGLE_ACCURACY = 5
SHADOW_OFFSET = 10

def rotate_around_point(x,y, angle):
    ra = math.radians(angle)
    s = math.sin(ra)
    c = math.cos(ra)

    x_new = float(x) * c - float(y) * s
    y_new = float(x) * s + float(y) * c

    return x_new, y_new

class Piece(object):
    def __init__(self,game,row,col,image, shadow_image, x_offset, y_offset):
        self.game = game
        self.row = row
        self.col = col
        self.image = image
        self.shadow_image = shadow_image

        self.x_offset = x_offset
        self.y_offset = y_offset
 
        self.width = image.get_width()
        self.height = image.get_height()
        self.cx = self.width / 2
        self.cy = self.height / 2
        self.angle = 0.0
        self.dragging = False
        self.in_position = False # is it in correct position in puzzle?

        # save original values for checking when a piece is back in position
        self.original_x_offset = self.x_offset
        self.original_y_offset = self.y_offset
        self.original_angle = self.angle
        # polygon to render correct location for piece
        self.click_polygon = self.create_click_polygon()
        self.position_polygon = self.create_position_polygon()

    def check_position(self):
        """
        Checks if piece is in correct location and rotation
        within a given accuracy
        """
        self.min_x_offset = self.game.pos_cx + self.original_x_offset - LOCATION_ACCURACY
        self.min_y_offset = self.game.pos_cy +self.original_y_offset - LOCATION_ACCURACY
        self.max_x_offset = self.game.pos_cx + self.original_x_offset + LOCATION_ACCURACY
        self.max_y_offset = self.game.pos_cy +self.original_y_offset + LOCATION_ACCURACY
        self.min_angle = self.original_angle - ANGLE_ACCURACY % 360
        self.max_angle = self.original_angle + ANGLE_ACCURACY % 360

        if self.min_x_offset <= self.x_offset  and self.max_x_offset >= self.x_offset and self.min_y_offset <= self.y_offset and self.max_y_offset >= self.y_offset and self.min_angle <= self.angle and self.max_angle >= self.angle:
                self.in_position = True
                # snap to correct pos
                self.x_offset = self.original_x_offset + self.game.pos_cx
                self.y_offset = self.original_y_offset + self.game.pos_cy
                self.angle = self.original_angle
                self.game.paper_sound.play(0)
                self.stop_dragging()
                return True
        return False


    def drag(self, delta):
        if self.in_position:
            # already in position, no more dragging
            return

        self.x_offset += (delta[0] / self.game.scale)
        self.y_offset += (delta[1] / self.game.scale)
        #self.update_polygon()

        # check if in correct location
        return self.check_position()
    
    def move(self, delta, angle):
        self.drag(delta)
        self.angle = angle

    def render(self, screen):
        # rotate image

        rotated_image = pygame.transform.rotozoom(self.image, -self.angle, self.game.scale)

        if self.in_position:
            image_pos_x = self.original_x_offset + self.game.pos_cx + self.cx
            image_pos_y = self.original_y_offset + self.game.pos_cy + self.cy
            rotated_shadow = None
        else:
            image_pos_x = self.x_offset + self.cx
            image_pos_y = self.y_offset + self.cy
            rotated_shadow = pygame.transform.rotozoom(self.shadow_image, -self.angle, self.game.scale)

        image_cx = float(image_pos_x + self.cx) * self.game.scale
        image_cy = float(image_pos_y + self.cy) * self.game.scale


        rotated_cx =  image_cx - rotated_image.get_width() /2
        rotated_cy =  image_cy - rotated_image.get_height() /2 
        if rotated_shadow:
            screen.blit(rotated_shadow,(rotated_cx+SHADOW_OFFSET, rotated_cy+SHADOW_OFFSET))

        screen.blit(rotated_image,(rotated_cx, rotated_cy))

        self.render_border(screen)
        self.render_centre(screen)

    def render_centre(self,screen):
        """
        Renders a cross in the centre of the puzzle piece
        """
        return
        # cx = float(self.x_offset + self.cx * 2) * self.game.scale
        # cy = float(self.y_offset + self.cy * 2) * self.game.scale

        # pygame.draw.line(screen, GREEN, [cx, cy], [cx + CENTRE_CROSS_SIZE, cy], 1)
        # pygame.draw.line(screen, GREEN, [cx, cy], [cx - CENTRE_CROSS_SIZE, cy], 1)
        # pygame.draw.line(screen, GREEN, [cx, cy], [cx, cy + CENTRE_CROSS_SIZE], 1)
        # pygame.draw.line(screen, GREEN, [cx, cy], [cx, cy - CENTRE_CROSS_SIZE], 1)

    def render_border(self,screen):
        """
        Renders a border around the edges of the puzzle piece
        """
        colour = BLACK
        width = 1
        if self.in_position:
            colour = GREEN
            self.position_polygon = self.create_position_polygon()
            self.rotated_polygon = self.position_polygon.rotate(math.radians(self.angle))
        else:
            if self.dragging:
                colour = RED
                width = 3
            self.click_polygon = self.create_click_polygon()
            self.rotated_polygon = self.click_polygon.rotate(math.radians(self.angle))

        pygame.draw.polygon(screen, colour, self.rotated_polygon, 1)

    def render_position(self,screen):
        """
        Render border for original position of piece
        """
        self.position_polygon = self.create_position_polygon()
        pygame.draw.polygon(screen, GREY, self.position_polygon, 1)

    def rotate_left(self):
        if self.in_position:
            # already in position, no more rotating
            return

        self.angle -= ROTATION_SPEED
        self.angle = self.angle % 360
        return self.check_position()

    def rotate_right(self):
        if self.in_position:
            # already in position, no more rotating
            return

        self.angle += ROTATION_SPEED
        self.angle = self.angle % 360
        return self.check_position()

    def start_dragging(self):
        self.dragging = True

    def stop_dragging(self):
        self.dragging = False
       

    def create_click_polygon(self):
        x = float(self.x_offset + self.cx) * self.game.scale
        y = float(self.y_offset + self.cy) * self.game.scale
        width = float(self.width) * self.game.scale
        height = float(self.height) * self.game.scale
        points = []
        
        points.append((x, y))
        points.append((x + width, y))
        points.append((x + width, y + height))
        points.append((x, y + height))

        return Polygon(points)

    def create_position_polygon(self):
        x = float(self.original_x_offset + self.cx + self.game.pos_cx) * self.game.scale
        y = float(self.original_y_offset + self.cy + self.game.pos_cy) * self.game.scale
        width = float(self.width) * self.game.scale
        height = float(self.height) * self.game.scale
        points = []
        
        points.append((x, y))
        points.append((x + width, y))
        points.append((x + width, y + height))
        points.append((x, y + height))

        return Polygon(points)
