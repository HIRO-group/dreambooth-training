import pyglet
import numpy as np
from pyglet.gl import *
import math
import OpenGL.GL as gl

# Define colors
_BLACK = (0, 0, 0)
_WHITE = (255, 255, 255)
_DARKSLATEBLUE = (72, 61, 139)
_SKY_BLUE = (135, 206, 235)
_TEAL = (0, 128, 128)
_DARKORANGE = (255, 140, 0)
_RED = (255, 0, 0)
_GOAL_COLOR = (60, 60, 60)
_PINK = (255, 192, 203)  # Define color for workstations
_ORANGE = (255, 165, 0)  # Define color for home locations

_BACKGROUND_COLOR = _WHITE
_GRID_COLOR = _BLACK
_SHELF_COLOR = _BLACK
_ENDPOINT_COLOR = _SKY_BLUE
_WORKSTATION_COLOR = _PINK
_HOME_COLOR = _ORANGE
_AGENT_COLOR = _DARKORANGE
_AGENT_LOADED_COLOR = _RED
_AGENT_DIR_COLOR = _BLACK

# Define the layout
layout = """
..x@.......@..
..@.@@.@..@x..
.@.@xx@x@..@@.
.xx@@@...@..x.
.@@.@x@x.x..@.
..x..@.@@@@x@.
.@@.@@.@x.@@..
.x.@xx@@x@xx..
.@.........@..
"""

# Parse the layout
layout = layout.strip().split("\n")
rows = len(layout)
cols = len(layout[0])

# Define the size of each cell
cell_size = 30

# Create a window without padding
window = pyglet.window.Window(
    width=cols * (cell_size + 1),
    height=rows * (cell_size + 1)
)

# Create a batch for efficient rendering
batch = pyglet.graphics.Batch()

# Create shapes based on the layout
shelves = []
goals = []
endpoints = []
workstations = []
home_locations = []
for y, row in enumerate(layout):
    for x, char in enumerate(row):
        if char == 'x':
            shelves.append((x, y))
        elif char == 'g':
            goals.append((x, y))
        elif char == '@':
            endpoints.append((x, y))
        elif char == 'w':
            workstations.append((x, y))
        elif char == 'h':
            home_locations.append((x, y))

# Normalize color values to [0, 1]
def normalize_color(color):
    return tuple(c / 255.0 for c in color)

@window.event
def on_draw():
    window.clear()
    gl.glClearColor(*normalize_color(_BACKGROUND_COLOR), 1.0)  # Normalize and set alpha to 1.0
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    window.switch_to()
    window.dispatch_events()

    # Draw grid
    batch = pyglet.graphics.Batch()
    for r in range(rows + 1):
        batch.add(
            2,
            gl.GL_LINES,
            None,
            (
                "v2f",
                (
                    0,  # LEFT X
                    (cell_size + 1) * r + 1,  # Y
                    (cell_size + 1) * cols,  # RIGHT X
                    (cell_size + 1) * r + 1,  # Y
                ),
            ),
            ("c3B", (*_GRID_COLOR, *_GRID_COLOR)),
        )
    for c in range(cols + 1):
        batch.add(
            2,
            gl.GL_LINES,
            None,
            (
                "v2f",
                (
                    (cell_size + 1) * c + 1,  # X
                    0,  # BOTTOM Y
                    (cell_size + 1) * c + 1,  # X
                    (cell_size + 1) * rows,  # TOP Y
                ),
            ),
            ("c3B", (*_GRID_COLOR, *_GRID_COLOR)),
        )
    batch.draw()

    # Draw shelves
    batch = pyglet.graphics.Batch()
    for x, y in shelves:
        y = rows - y - 1  # pyglet rendering is reversed
        batch.add(
            4,
            gl.GL_QUADS,
            None,
            (
                "v2f",
                (
                    (cell_size + 1) * x + 1,  # TL - X
                    (cell_size + 1) * y + 1,  # TL - Y
                    (cell_size + 1) * (x + 1),  # TR - X
                    (cell_size + 1) * y + 1,  # TR - Y
                    (cell_size + 1) * (x + 1),  # BR - X
                    (cell_size + 1) * (y + 1),  # BR - Y
                    (cell_size + 1) * x + 1,  # BL - X
                    (cell_size + 1) * (y + 1),  # BL - Y
                ),
            ),
            ("c3B", 4 * _SHELF_COLOR),
        )
    batch.draw()

    # Draw goals
    batch = pyglet.graphics.Batch()
    for x, y in goals:
        y = rows - y - 1  # pyglet rendering is reversed
        batch.add(
            4,
            gl.GL_QUADS,
            None,
            (
                "v2f",
                (
                    (cell_size + 1) * x + 1,  # TL - X
                    (cell_size + 1) * y + 1,  # TL - Y
                    (cell_size + 1) * (x + 1),  # TR - X
                    (cell_size + 1) * y + 1,  # TR - Y
                    (cell_size + 1) * (x + 1),  # BR - X
                    (cell_size + 1) * (y + 1),  # BR - Y
                    (cell_size + 1) * x + 1,  # BL - X
                    (cell_size + 1) * (y + 1),  # BL - Y
                ),
            ),
            ("c3B", 4 * _GOAL_COLOR),
        )
    batch.draw()

    # Draw endpoints
    batch = pyglet.graphics.Batch()
    for x, y in endpoints:
        y = rows - y - 1  # pyglet rendering is reversed
        batch.add(
            4,
            gl.GL_QUADS,
            None,
            (
                "v2f",
                (
                    (cell_size + 1) * x + 1,  # TL - X
                    (cell_size + 1) * y + 1,  # TL - Y
                    (cell_size + 1) * (x + 1),  # TR - X
                    (cell_size + 1) * y + 1,  # TR - Y
                    (cell_size + 1) * (x + 1),  # BR - X
                    (cell_size + 1) * (y + 1),  # BR - Y
                    (cell_size + 1) * x + 1,  # BL - X
                    (cell_size + 1) * (y + 1),  # BL - Y
                ),
            ),
            ("c3B", 4 * _ENDPOINT_COLOR),
        )
    batch.draw()

    # Draw workstations
    batch = pyglet.graphics.Batch()
    for x, y in workstations:
        y = rows - y - 1  # pyglet rendering is reversed
        batch.add(
            4,
            gl.GL_QUADS,
            None,
            (
                "v2f",
                (
                    (cell_size + 1) * x + 1,  # TL - X
                    (cell_size + 1) * y + 1,  # TL - Y
                    (cell_size + 1) * (x + 1),  # TR - X
                    (cell_size + 1) * y + 1,  # TR - Y
                    (cell_size + 1) * (x + 1),  # BR - X
                    (cell_size + 1) * (y + 1),  # BR - Y
                    (cell_size + 1) * x + 1,  # BL - X
                    (cell_size + 1) * (y + 1),  # BL - Y
                ),
            ),
            ("c3B", 4 * _WORKSTATION_COLOR),
        )
    batch.draw()

    # Draw home locations
    batch = pyglet.graphics.Batch()
    for x, y in home_locations:
        y = rows - y - 1  # pyglet rendering is reversed
        batch.add(
            4,
            gl.GL_QUADS,
            None,
            (
                "v2f",
                (
                    (cell_size + 1) * x + 1,  # TL - X
                    (cell_size + 1) * y + 1,  # TL - Y
                    (cell_size + 1) * (x + 1),  # TR - X
                    (cell_size + 1) * y + 1,  # TR - Y
                    (cell_size + 1) * (x + 1),  # BR - X
                    (cell_size + 1) * (y + 1),  # BR - Y
                    (cell_size + 1) * x + 1,  # BL - X
                    (cell_size + 1) * (y + 1),  # BL - Y
                ),
            ),
            ("c3B", 4 * _HOME_COLOR),
        )
    batch.draw()

    # Save the image to a custom folder with a descriptive name
    import os
    
    # Create a folder named 'warehouse_layouts' if it doesn't exist
    save_folder = 'valid_warehouse_layouts'
    os.makedirs(save_folder, exist_ok=True)
    
    # Generate a descriptive filename
    filename = f'valid warehouse layouts: map elites paper 12.png'
    
    # Combine the folder and filename
    save_path = os.path.join(save_folder, filename)
    
    # Save the image
    pyglet.image.get_buffer_manager().get_color_buffer().save(save_path)
    
    print(f"Warehouse layout saved as: {save_path}")

# Run the application
pyglet.app.run()
