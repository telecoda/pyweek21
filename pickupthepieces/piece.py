import pygame
import math
from pylygon import Polygon

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

CENTRE_CROSS_SIZE = 10

ROTATION_SPEED = 5

LOCATION_ACCURACY = 10
ANGLE_ACCURACY = 5

def rotate_around_point(x,y, angle):
    ra = math.radians(angle)
    s = math.sin(ra)
    c = math.cos(ra)

    x_new = float(x) * c - float(y) * s
    y_new = float(x) * s + float(y) * c

    return x_new, y_new

class Piece(object):
    def __init__(self,row,col,image, x_offset, y_offset):
        self.row = row
        self.col = col
        self.image = image

        self.x_offset = x_offset
        self.y_offset = y_offset
 
        self.width = image.get_width()
        self.height = image.get_height()
        self.cx = self.width / 2
        self.cy = self.height / 2
        self.angle = 0.0
        self.update_polygon()
        self.dragging = False
        self.in_position = False # is it in correct position in puzzle?

        # save original values for checking when a piece is back in position
        self.original_x_offset = self.x_offset
        self.original_y_offset = self.y_offset
        self.original_angle = self.angle
        self.min_x_offset = self.x_offset - LOCATION_ACCURACY
        self.min_y_offset = self.y_offset - LOCATION_ACCURACY
        self.max_x_offset = self.x_offset + LOCATION_ACCURACY
        self.max_y_offset = self.y_offset + LOCATION_ACCURACY
        self.min_angle = self.angle - ANGLE_ACCURACY % 360
        self.max_angle = self.angle + ANGLE_ACCURACY % 360

    def check_position(self):
        """
        Checks if piece is in correct location and rotation
        within a given accuracy
        """
        if self.min_x_offset <= self.x_offset  and self.max_x_offset >= self.x_offset and self.min_y_offset <= self.y_offset and self.max_y_offset >= self.y_offset and self.min_angle <= self.angle and self.max_angle >= self.angle:
                self.in_position = True
                # snap to correct pos
                self.x_offset = self.original_x_offset
                self.y_offset = self.original_y_offset
                self.angle = self.original_angle
                self.update_polygon()
                self.stop_dragging()


    def drag(self, delta):
        if self.in_position:
            # already in position, no more dragging
            return

        self.x_offset += delta[0]
        self.y_offset += delta[1]
        self.update_polygon()

        # check if in correct location
        self.check_position()
    
    def move(self, delta, angle):
        self.drag(delta)
        self.angle = angle

    def render(self, screen):
        # rotate image

        rotated_image = pygame.transform.rotate(self.image,-self.angle)

        image_pos_x = self.x_offset + self.cx
        image_pos_y = self.y_offset + self.cy

        image_cx = image_pos_x + self.cx
        image_cy = image_pos_y + self.cy

        rotated_cx =  image_cx - rotated_image.get_width() /2
        rotated_cy =  image_cy - rotated_image.get_height() /2 
        screen.blit(rotated_image,(rotated_cx, rotated_cy))

        self.render_border(screen)
        self.render_centre(screen)

    def render_centre(self,screen):
        """
        Renders a cross in the centre of the puzzle piece
        """
        cx = self.x_offset + self.cx * 2
        cy = self.y_offset + self.cy * 2

        pygame.draw.line(screen, GREEN, [cx, cy], [cx + CENTRE_CROSS_SIZE, cy], 5)
        pygame.draw.line(screen, GREEN, [cx, cy], [cx - CENTRE_CROSS_SIZE, cy], 5)
        pygame.draw.line(screen, GREEN, [cx, cy], [cx, cy + CENTRE_CROSS_SIZE], 5)
        pygame.draw.line(screen, GREEN, [cx, cy], [cx, cy - CENTRE_CROSS_SIZE], 5)

    def render_border(self,screen):
        """
        Renders a border around the edges of the puzzle piece
        """
        self.rotated_polygon = self.original_polygon.rotate(math.radians(self.angle))
        colour = BLACK
        if self.in_position:
            colour = GREEN
        if self.dragging:
            colour = RED

        pygame.draw.polygon(screen, colour, self.rotated_polygon, 5)


    def rotate_left(self):
        if self.in_position:
            # already in position, no more rotating
            return

        self.angle -= ROTATION_SPEED
        self.angle = self.angle % 360

    def rotate_right(self):
        if self.in_position:
            # already in position, no more rotating
            return

        self.angle += ROTATION_SPEED
        self.angle = self.angle % 360

    def start_dragging(self):
        self.dragging = True

    def stop_dragging(self):
        self.dragging = False
       

    def update_polygon(self):
        x = self.x_offset + self.cx
        y = self.y_offset + self.cy
        width = self.width
        height = self.height
        points = []
        
        points.append((x, y))
        points.append((x + width, y))
        points.append((x + width, y + height))
        points.append((x, y + height))

        self.original_polygon = Polygon(points)

