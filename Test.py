import pygame
import numpy as np

# Pygame initialization
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Autonomous Vehicle Simulation")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Vehicle properties
vehicle_pos = np.array([400, 300])
vehicle_angle = 0
vehicle_speed = 5
turning_rate = 5

# Define checkpoints
checkpoints = [np.array([400 + 150 * np.cos(np.pi / 4 * i), 300 + 150 * np.sin(np.pi / 4 * i)]) for i in range(8)]
current_checkpoint_index = 0

# Obstacle properties
obstacles = [np.array([400 + 100 * np.cos(np.pi / 4 * i), 300 + 100 * np.sin(np.pi / 4 * i)]) for i in range(2, 8)]

# Visualization paths
paths = []

# Steering wheel properties
steering_wheel_center = (700, 550)
steering_wheel_radius = 30

def draw_vehicle(pos, angle):
    rotated_vehicle = pygame.transform.rotate(pygame.Surface((20, 10), pygame.SRCALPHA), -angle)
    rect = rotated_vehicle.get_rect(center=pos)
    screen.blit(rotated_vehicle, rect.topleft)

def draw_steering_wheel(angle):
    # Draw the steering wheel
    pygame.draw.circle(screen, WHITE, steering_wheel_center, steering_wheel_radius, 5)
    # Draw the steering wheel handle
    handle_length = 20
    handle_x = steering_wheel_center[0] + handle_length * np.cos(np.radians(angle))
    handle_y = steering_wheel_center[1] - handle_length * np.sin(np.radians(angle))
    pygame.draw.line(screen, WHITE, steering_wheel_center, (handle_x, handle_y), 5)

def check_obstacle_collision(vehicle_pos, obstacles):
    for obs in obstacles:
        if np.linalg.norm(vehicle_pos - obs) < 15:  # Collision detection
            return True
    return False

def move_vehicle():
    global vehicle_pos, vehicle_angle, paths, current_checkpoint_index

    # Check for obstacle collision
    if check_obstacle_collision(vehicle_pos, obstacles):
        vehicle_pos -= 2 * np.array([np.cos(np.radians(vehicle_angle)), np.sin(np.radians(vehicle_angle))])  # Move back if colliding
    else:
        # Move forward
        vehicle_pos += np.array([np.cos(np.radians(vehicle_angle)), np.sin(np.radians(vehicle_angle))]) * vehicle_speed

        # Store the path
        paths.append(vehicle_pos.copy())

    # Check if reached the checkpoint
    if np.linalg.norm(vehicle_pos - checkpoints[current_checkpoint_index]) < 10:
        current_checkpoint_index = (current_checkpoint_index + 1) % len(checkpoints)  # Move to next checkpoint

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        vehicle_angle += turning_rate
    if keys[pygame.K_RIGHT]:
        vehicle_angle -= turning_rate

    move_vehicle()

    # Drawing
    screen.fill(BLACK)

    # Draw paths
    if len(paths) > 1:
        for i in range(len(paths) - 1):
            pygame.draw.line(screen, GREEN, paths[i].astype(int), paths[i + 1].astype(int), 3)

    # Draw checkpoints
    for checkpoint in checkpoints:
        pygame.draw.circle(screen, GREEN, checkpoint.astype(int), 10)

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.circle(screen, RED, obs.astype(int), 10)

    # Draw the vehicle
    draw_vehicle(vehicle_pos.astype(int), vehicle_angle)

    # Draw the steering wheel
    draw_steering_wheel(vehicle_angle)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
