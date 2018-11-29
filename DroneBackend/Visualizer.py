import pygame
import math

class Visualizer:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen_offset = 10

        self.min_x = math.inf
        self.min_y = math.inf
        self.max_x = -math.inf
        self.max_y = -math.inf

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Drone Simulator")
        pygame.display.flip()

    def init_markers(self,markers):
        for marker in markers:
            x = marker.x
            y = marker.y
            if x > self.max_x:
                self.max_x = x
            if y > self.max_y:
                self.max_y = y
            if x < self.min_x:
                self.min_x = x
            if y < self.min_y:
                self.min_y = y

    def get_delta(self, marker):
        distance_x = marker.x - self.min_x
        distance_y = marker.y - self.min_y

        total_distance_x = self.max_x - self.min_x
        total_distance_y = self.max_y - self.min_y

        delta_x = distance_x/total_distance_x
        delta_y = distance_y/total_distance_y

        return[delta_x, delta_y]

    def draw_markers(self, markers):
        for marker in markers:
            [delta_x, delta_y] = self.get_delta(marker)

            pos_x = int(self.width * delta_x)
            pos_y = int(self.height * delta_y)

            if pos_x < 250:
                pos_x += self.screen_offset
            if pos_y < 250:
                pos_y += self.screen_offset

            if pos_x > 250:
                pos_x -= self.screen_offset

            if pos_y > 250:
                pos_y -= self.screen_offset

            pygame.draw.circle(self.screen, (0, 0, 255), (pos_x, pos_y), 5)
            pygame.display.update()

    def quit_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False
