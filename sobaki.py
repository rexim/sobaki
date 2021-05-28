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

    def render(self, screen, pos):
        image = loading_image
        if self.future.done():
            image = self.future.result()
        screen.blit(image, pos)
        return image.get_height()

pygame.init()

with ThreadPoolExecutor(max_workers=100) as executor:
    doggos = [DoggoImage(executor) for i in range(10)]
    running = True
    scroll_y = 0
    scroll_step = 100
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    scroll_y -= scroll_step
                elif event.key == pygame.K_w:
                    scroll_y += scroll_step

        screen.fill((255, 255, 255))

        y = scroll_y
        for doggo in doggos:
            y += doggo.render(screen, (0, y))

        pygame.display.flip()

pygame.quit()
