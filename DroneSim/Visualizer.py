
import pygame


class Visualizer:

    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Drone Simulator")
        pygame.display.flip()

    def initialze_coordinate_system(self,markers):
        """
        Initialze the coordinate system, set the devide factors
        :param markers: the map markers
        :return:
        """
        try: assert(len(markers) > 1)    # more than 1 marker is needed to calculate a coordinate system
        except AssertionError:
            print("More than 1 marker needed to calculate coordinate system.")
            return False

        l_x = 0
        l_y = 0
        for marker in markers:
            l_x = abs(marker[0]) if abs(marker[0]) > l_x else l_x
            l_y = abs(marker[1]) if abs(marker[1]) > l_y else l_y

        self.x_offset = int(0.15 * self.width)
        self.y_offset = int(0.15 * self.height)

        self.x_scale = (self.width - self.x_offset) / 2 * l_x
        self.y_scale = (self.height - self.y_offset) / 2 * l_y
        return True

    def draw_markers(self,markers):
        for marker in markers:
            pos_x = int(self.width / 2 - marker[0] * self.x_scale)
            pos_y = int(self.height / 2 - marker[1] * self.y_scale)
            pygame.draw.circle(self.screen, (0,0,255), (pos_x, pos_y), 25)
        pygame.display.update()

    def quit_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False
