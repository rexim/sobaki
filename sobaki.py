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
    scroll_step = 100
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    scroll_y -= scroll_step
                elif event.key == pygame.K_w:
                    scroll_y = min(scroll_y + scroll_step, 0)

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
