import pygame
import math
import serial
import serial.tools.list_ports

# ---------------------------
# Auto-detect available COM ports
# ---------------------------
ports = list(serial.tools.list_ports.comports())
if not ports:
    print("No COM ports found! Connect your Arduino.")
    exit()

print("Available COM ports:")
for i, port in enumerate(ports):
    print(f"{i}: {port.device}")

port_index = int(input("Select the COM port index: "))
COM_PORT = ports[port_index].device
BAUD_RATE = 9600

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
print(f"Connected to {COM_PORT} at {BAUD_RATE} baud")

# ---------------------------
# Pygame Setup
# ---------------------------
WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Triangular Prism Controlled by MPU6050")
clock = pygame.time.Clock()

# ---------------------------
# Triangular Prism Definition
# ---------------------------
prism_vertices = [
    [-1, -1, -1], [1, -1, -1], [0, 1, -1],   # bottom triangle
    [-1, -1, 1], [1, -1, 1], [0, 1, 1]       # top triangle
]

prism_faces = [
    (0, 1, 2),       # bottom triangle
    (3, 4, 5),       # top triangle
    (0, 1, 4, 3),    # side rectangle
    (1, 2, 5, 4),    # side rectangle
    (2, 0, 3, 5)     # side rectangle
]

face_colors = [
    (255, 0, 0),     # bottom
    (0, 255, 0),     # top
    (0, 0, 255),     # side 1
    (255, 255, 0),   # side 2
    (0, 255, 255)    # side 3
]

SCALE = 100
OFFSET_X, OFFSET_Y = WIDTH // 2, HEIGHT // 2

# ---------------------------
# Functions
# ---------------------------
def rotate_point(x, y, z, ax, ay, az):
    # Rotate around X-axis
    cosx, sinx = math.cos(ax), math.sin(ax)
    y, z = y * cosx - z * sinx, y * sinx + z * cosx
    # Rotate around Y-axis
    cosy, siny = math.cos(ay), math.sin(ay)
    x, z = x * cosy + z * siny, -x * siny + z * cosy
    # Rotate around Z-axis
    cosz, sinz = math.cos(az), math.sin(az)
    x, y = x * cosz - y * sinz, x * sinz + y * cosz
    return x, y, z

def project(x, y, z):
    factor = SCALE / (z + 5)
    x_proj = x * factor + OFFSET_X
    y_proj = -y * factor + OFFSET_Y
    return int(x_proj), int(y_proj)

# ---------------------------
# Main Loop
# ---------------------------
ax = ay = az = 0.0
running = True

while running:
    screen.fill((0, 0, 0))

    # Read Arduino data
    if ser.in_waiting:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                ax_raw, ay_raw, az_raw, gx, gy, gz = map(int, line.split(","))
                ax = math.radians(ax_raw / 16384 * 90)
                ay = math.radians(ay_raw / 16384 * 90)
                az = math.radians(az_raw / 16384 * 90)
        except:
            pass

    # Rotate vertices
    transformed_vertices = [rotate_point(*v, ax, ay, az) for v in prism_vertices]

    # Sort faces by depth (Painter's Algorithm)
    face_depths = [(i, sum(transformed_vertices[v][2] for v in face)/len(face))
                   for i, face in enumerate(prism_faces)]
    face_depths.sort(key=lambda x: x[1], reverse=True)

    # Draw faces
    for face_index, _ in face_depths:
        face = prism_faces[face_index]
        points = [project(*transformed_vertices[v]) for v in face]
        pygame.draw.polygon(screen, face_colors[face_index], points)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
ser.close()
