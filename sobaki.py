#!/usr/bin/env python3

import requests
import json
import io
import pygame
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

screen = pygame.display.set_mode([500, 500], pygame.RESIZABLE)

loading_image = pygame.image.load('./loading.jpg')

def fetch_random_dogo_image():
    r = requests.get('https://dog.ceo/api/breeds/image/random')
    r = requests.get(r.json()['message'])
    image = Image.open(io.BytesIO(r.content))
    return pygame.image.fromstring(image.tobytes(), image.size, image.mode)

class DoggoImage:
    def __init__(self, executor):
        self.future = executor.submit(fetch_random_dogo_image)

    def image(self):
        image = loading_image
        if self.future.done():
            image = self.future.result()
        return image

pygame.init()

with ThreadPoolExecutor(max_workers=100) as executor:
    doggos = []
    running = True
    scroll_y = 0
    scroll_dy = 0
    scroll_step = 10000.0
    last_ticks = pygame.time.get_ticks()

    hold_pos = None
    while running:
        t = pygame.time.get_ticks()
        delta_time = (last_ticks - t) / 1000.0
        last_ticks = t

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                hold_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                hold_pos = None
                scroll_dy *= -300.0
            elif event.type == pygame.MOUSEMOTION:
                if hold_pos is not None:
                    scroll_dy = event.pos[1] - hold_pos[1]
                    scroll_y += scroll_dy
                    hold_pos = event.pos

        if hold_pos is None:
            scroll_y = scroll_y + scroll_dy * delta_time
            scroll_dy = scroll_dy * 0.95
            if abs(scroll_dy) < 0.001:
                scroll_dy = 0.0

        w, h = screen.get_size()

        screen.fill((255, 255, 255))

        y = scroll_y
        for doggo in doggos:
            if y >= h: break

            image = doggo.image()

            if y + image.get_height() >= 0:
                screen.blit(image, (0, y))

            y += image.get_height()

        if y < h:
            doggos.append(DoggoImage(executor))

        pygame.display.flip()

pygame.quit()
