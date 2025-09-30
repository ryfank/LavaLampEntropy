# lava_blobs.py
# simple lava lamp simulator that generates random hashes
# using the visual state of the blobs 
# mini version of Cloudflare's lavarand

import pygame
import random
import hashlib
import threading
from flask import Flask, jsonify, send_from_directory
import math

#Flask setup
# flask is just used to serve the web page and give the entropy value
app = Flask(__name__, static_folder='../web')

# Pygame setup 
WIDTH, HEIGHT = 500, 400
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lava Lamp")  # Window title
clock = pygame.time.Clock()  

# blob class
# Each "blob" is like a blob of lava that moves around
class Blob:
    # Some colors that look like lava
    LAVA_COLORS = [
        (255, 69, 0),    # red-orange
        (255, 140, 0),   # dark orange
        (255, 165, 0),   # orange
        (255, 180, 50),  # softer yellow-orange
        (255, 99, 71),   # tomato red
    ]

    def __init__(self):
        # Random starting position
        self.x = random.randint(30, WIDTH - 30)
        self.y = random.randint(30, HEIGHT - 30)
        # Random speed
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        # Random size so blobs are different
        self.size = random.randint(15, 35)
        # Pick a random lava color and add some variation
        base = random.choice(self.LAVA_COLORS)
        self.color = [min(255, max(0, c + random.randint(-20, 20))) for c in base]
        # Noise offset helps make movement feel more wobbly and organic
        self.noise_offset = random.uniform(0, 1000)

    # Move the blob each frame
    def move(self):
        # Add sine + small offsets for smooth wobbly motion
        self.x += self.vx + math.sin(self.noise_offset)/2
        self.y += self.vy + math.cos(self.noise_offset)/2
        self.noise_offset += 0.05

        #  function to bounce off walls
        if self.x - self.size < 0: #left edge
            self.x = self.size
            self.vx *= -1
    #object’s left edge has moved past x=0 
    # (the left border of the screen)
        if self.x + self.size > WIDTH: # right edge
            self.x = WIDTH - self.size
            self.vx *= -1
            #the right edge of the object
        if self.y - self.size < 0: #top edge
            self.y = self.size
            self.vy *= -1

            #bottom edge
        if self.y + self.size > HEIGHT:  #greater than HEIGHT, object crossed the bottom boundary
            self.y = HEIGHT - self.size
            self.vy *= -1
            #if falling down, now bounces up
           

    # Draw the blob on the screen
    def draw(self, surface):
        # making a glowing blob
        gradient_surface = pygame.Surface((self.size*4, self.size*4), pygame.SRCALPHA)
        center = self.size*2
        for r in range(self.size*2, 0, -1):
            alpha = max(0, 255 * (r / (self.size*2))**2)  # soft edges
            color = [min(255, c + 50) for c in self.color]  # brighten the color for glow
            pygame.draw.circle(gradient_surface, (*color, int(alpha)), (center, center), r)
        surface.blit(gradient_surface, (int(self.x - center), int(self.y - center)), special_flags=pygame.BLEND_ADD)

# Make a bunch of blobs
blobs = [Blob() for _ in range(10)]

# Entropy function
# turn whatever you see on screen into a hash
def get_entropy(surface):
    raw = pygame.image.tostring(surface, "RGB")
    return hashlib.sha256(raw).hexdigest()

# Flask routes
@app.route("/")
def index():
    # serve the HTML page
    return send_from_directory(app.static_folder, "index.html")

@app.route("/entropy")
def entropy_api():
    # Return the hash of the current screen as JSON
    return jsonify({"entropy": get_entropy(screen)})

# Run Flask in the background
def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# Main Pygame loop
def run():
    # Start flask server in a separate thread
    threading.Thread(target=run_flask, daemon=True).start()
    running = True
    while running:
        screen.fill((10, 5, 15))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #move and draw all blobs
        for blob in blobs:
            blob.move()
            blob.draw(screen)

        pygame.display.flip()  # Show it on screen
        clock.tick(30)  # 30 frames per second

    pygame.quit()

# run the lava lamp
if __name__ == "__main__":
    run()
