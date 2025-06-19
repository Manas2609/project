import pygame, math, array

# Generate siren sound
def generate_siren(freq1=400, freq2=800, duration=0.5, volume=0.5, sample_rate=44100):
    num_samples = int(duration * sample_rate)
    buf = array.array('h', [0] * num_samples)
    for i in range(num_samples):
        t = i / sample_rate
        freq = freq1 if int(t * 2) % 2 == 0 else freq2
        buf[i] = int(volume * 32767 * math.sin(2 * math.pi * freq * t))
    return pygame.mixer.Sound(buffer=buf)

# Initialize pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Forest Animal Boundary Alert")
clock = pygame.time.Clock()

# Colors
GREEN = (34, 139, 34)
RED = (255, 0, 0)

# Load siren
siren = generate_siren()

# Animal class
class Animal:
    def __init__(self, image_path, start_pos):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=start_pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def touches_boundary(self):
        return (
            self.rect.left <= 10 or
            self.rect.right >= width - 10 or
            self.rect.top <= 10 or
            self.rect.bottom >= height - 10
        )

# List of images and positions
image_files = ['monkey.png', 'lion.png', 'elephant.png', 'dog.png', 'deer.png']
start_positions = [(150, 150), (300, 200), (450, 150), (600, 250), (350, 350)]
animals = [Animal(img, pos) for img, pos in zip(image_files, start_positions)]

selected_index = 0  # default controlled animal

# Light variables
light_on = False
light_timer = 0

# Game loop
running = True
while running:
    screen.fill(GREEN)
    pygame.draw.rect(screen, RED, (10, 10, width - 20, height - 20), 5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Change controlled animal
        elif event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_5:
                selected_index = event.key - pygame.K_1

    # Move selected animal
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        animals[selected_index].move(-5, 0)
    if keys[pygame.K_RIGHT]:
        animals[selected_index].move(5, 0)
    if keys[pygame.K_UP]:
        animals[selected_index].move(0, -5)
    if keys[pygame.K_DOWN]:
        animals[selected_index].move(0, 5)

    # Draw and check for boundary
    boundary_touched = False
    for animal in animals:
        animal.draw(screen)
        if animal.touches_boundary():
            boundary_touched = True

    # Siren and blinking light
    if boundary_touched:
        if not pygame.mixer.get_busy():
            siren.play()

        light_timer += 1
        if (light_timer // 20) % 2 == 0:
            light_on = True
        else:
            light_on = False

        if light_on:
            pygame.draw.circle(screen, (255, 0, 0), (750, 50), 20)  # red blinking light
    else:
        siren.stop()
        light_timer = 0

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
