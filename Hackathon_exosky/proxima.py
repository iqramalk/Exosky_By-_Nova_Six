import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Define window dimensions
WIDTH, HEIGHT = 1000, 800
RIGHT_PANEL_WIDTH = 200  # Width for the star list panel
screen = pygame.display.set_mode((WIDTH + RIGHT_PANEL_WIDTH, HEIGHT))
pygame.display.set_caption("Star Chart")

# Load background image
background_image = pygame.image.load("sky_images/proxima_sky.jpeg")  # Replace with your image file path
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale to fit the window

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
YELLOW = (255, 255, 0)
DARK_GRAY = (50, 50, 50)  # Shadow color
BLACK = (0, 0, 0)

# Font for rendering text (smaller size now)
font = pygame.font.Font(None, 20)

# Define the exoplanet name
exoplanet_name = "From Proxima centauri b (Exoplanet)"


# Star data (x, y, size, name)
stars = [
    (10.98, 0, 3, "Acrux (crux 1)"),
    (10.35, 6.02, 3, "Mimosa (crux 5 with js)"),
    (1.56, 2.69, 3, "Gacrux (crux 4 with js)"),
    (0, 10.98, 3, "Delta Crucis (crux 3)"),
    (6.5, 4.5, 2, "joining star (crux 2)"),
    (0, 0, 4, "Proxima Centauri(carina 1)"),
    (3.34, 5, 4, "Canopus(carina 2)"),
    (6.85, -4, 4, "Avior(carina 3)"),
    (1.01, 7, 4, "Miaplacidus(carina 7)"),
    (12, -9, 4, "Aspidiske(carina 4)"),
    (1.13, 8, 4, "Kappa Carinae(carina 6)"),
    (1.10, -6, 4, "Lota Carinae(carina 5)"),
]
    

# List to store points clicked by the user to form constellations
constellation_points = []

# Zoom level
zoom_level = 1.0

# Axis range
axis_min, axis_max = -15, 15

# Center of the screen (where (0,0) in the world will be located)
screen_center_x = WIDTH // 2
screen_center_y = HEIGHT // 2

# Function to map star coordinates (world space) to screen space
def world_to_screen(x, y):
    screen_x = int(screen_center_x + (x / (axis_max - axis_min)) * WIDTH)
    screen_y = int(screen_center_y - (y / (axis_max - axis_min)) * HEIGHT)  # Inverted y-axis for screen
    return screen_x, screen_y

def display_exoplanet_name():
    text = font.render(exoplanet_name, True, YELLOW)
    screen.blit(text, (10, 10))


# Function to display star name and position on hover
def display_star_info(name, position):
    text = font.render(f"{name} ({int(position[0])}, {int(position[1])})", True, YELLOW)
    screen.blit(text, (position[0] + 10, position[1] - 20))  # Show name above the star

# Function to draw constellations
def draw_constellation(points):
    if len(points) > 1:
        for i in range(len(points) - 1):
            pygame.draw.line(screen, YELLOW, points[i], points[i + 1], 2)

# Function to draw axes
def draw_axes():
    pygame.draw.line(screen, WHITE, world_to_screen(axis_min, 0), world_to_screen(axis_max, 0), 2)  # X axis
    pygame.draw.line(screen, WHITE, world_to_screen(0, axis_min), world_to_screen(0, axis_max), 2)  # Y axis

    for x in range(axis_min, axis_max + 1):  # Draw X axis labels
        label = font.render(str(int(x)), True, WHITE)
        screen.blit(label, world_to_screen(x, 0))

    for y in range(axis_min, axis_max + 1):  # Draw Y axis labels
        label = font.render(str(int(y)), True, WHITE)
        screen.blit(label, world_to_screen(0, y))

# Function to draw the star list on the right panel
def draw_star_list():
    panel_x = WIDTH  # Start drawing after the star chart
    panel_y = 20  # Start a little below the top
    for i, star in enumerate(stars):
        name = star[3]
        text_color = WHITE
        text = font.render(name, True, text_color)
        screen.blit(text, (panel_x + 20, panel_y + i * 30))  # Vertical spacing between star names

# Main loop
def main():
    global zoom_level  # Allow zoom_level to be modified in this scope
    clock = pygame.time.Clock()
    running = True

    while running:
        # Draw background image
        screen.blit(background_image, (0, 0))

        # Display the exoplanet name at the top
        display_exoplanet_name()

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Draw axes
        draw_axes()

        # Draw stars with shadows and check if mouse is hovering over a star
        for star in stars:
            x, y, size, name = star
            zoomed_x = x * zoom_level
            zoomed_y = y * zoom_level
            zoomed_size = int(size * zoom_level)

            screen_x, screen_y = world_to_screen(zoomed_x, zoomed_y)

            pygame.draw.circle(screen, DARK_GRAY, (screen_x, screen_y), zoomed_size + 2)  # Shadow
            pygame.draw.circle(screen, WHITE, (screen_x, screen_y), zoomed_size)

            distance = math.sqrt((mouse_x - screen_x) ** 2 + (mouse_y - screen_y) ** 2)
            if distance < zoomed_size + 5:
                display_star_info(name, (screen_x, screen_y))  # Show name and position near the star

        # Draw the right panel with the list of stars
        pygame.draw.rect(screen, BLACK, (WIDTH, 0, RIGHT_PANEL_WIDTH, HEIGHT))  # Right panel background
        draw_star_list()

        # Draw the constellation lines
        draw_constellation(constellation_points)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Detect left mouse click to add star to constellation points
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for star in stars:
                    x, y, size, name = star
                    zoomed_x = x * zoom_level
                    zoomed_y = y * zoom_level
                    screen_x, screen_y = world_to_screen(zoomed_x, zoomed_y)
                    distance = math.sqrt((mouse_x - screen_x) ** 2 + (mouse_y - screen_y) ** 2)
                    if distance < zoomed_size + 5:
                        constellation_points.append((screen_x, screen_y))

            # Right-click clears the constellation
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                constellation_points.clear()  # Clear all lines

            # Zooming functionality
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # Zoom in
                    zoom_level *= 1.1
                if event.key == pygame.K_MINUS:  # Zoom out
                    zoom_level *= 0.9

        # Refresh screen
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()