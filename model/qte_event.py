import random
import time
import pygame

class QTEEvent:
    def __init__(self, duration=2):
        self.key = random.choice([pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e,
                                  pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j,
                                  pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o,
                                  pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t,
                                  pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y,
                                  pygame.K_z])
        self.start_time = None
        self.duration = duration
        self.success = False

    def start(self):
        self.start_time = time.time()

    def check_input(self, event):
        if self.start_time and (time.time() - self.start_time <= self.duration):
            if event.type == pygame.KEYDOWN:
                if event.key == self.key:
                    self.success = True
                    return True
                else:
                    return False
        return False

    def is_active(self):
        return self.start_time and (time.time() - self.start_time <= self.duration)

    def has_failed(self):
        return self.start_time and (time.time() - self.start_time > self.duration) and not self.success
