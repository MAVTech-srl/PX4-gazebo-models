#!/usr/bin/env python3

# ========================================
# CONFIGURATION - MODIFY ONLY HERE!
# ========================================

# Column parameters
NUM_COLUMNS = 100       # Total number of columns
SPACING = 5.0           # Distance between columns (meters)
COLUMN_WIDTH = 2        # Column width (meters)
COLUMN_HEIGHT = 20.0    # Column height (meters)
START_X = 10.0          # X position of first column

# World parameters
WORLD_NAME = "world_obstacle"   # World name (must match drone configuration)
GROUND_SIZE = 1000              # Ground plane size (meters)
LAYOUT = "random"               # "line", "grid", "circle", "random"

# Output file parameters
OUTPUT_FILE = f"{WORLD_NAME}.sdf"

# ========================================
# GENERATOR (do not modify below)
# ========================================

import math
import random

def generate_columns_sdf():
    """
    Generate SDF file with columns based on configured parameters
    """
    
    # SDF file header
    sdf_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<sdf version="1.9">
<world name="{WORLD_NAME}">
<physics type="ode">
<max_step_size>0.004</max_step_size>
<real_time_factor>1.0</real_time_factor>
<real_time_update_rate>250</real_time_update_rate>
</physics>
<gravity>0 0 -9.8</gravity>
<magnetic_field>6e-06 2.3e-05 -4.2e-05</magnetic_field>
<atmosphere type="adiabatic"/>
<scene>
<grid>false</grid>
<ambient>0.4 0.4 0.4 1</ambient>
<background>0.7 0.7 0.7 1</background>
<shadows>true</shadows>
</scene>

<!-- Ground Plane -->
<model name="ground_plane">
<static>true</static>
<link name="link">
<collision name="collision">
<geometry>
<plane>
<normal>0 0 1</normal>
<size>1 1</size>
</plane>
</geometry>
<surface>
<friction>
<ode/>
</friction>
<bounce/>
<contact/>
</surface>
</collision>
<visual name="visual">
<geometry>
<plane>
<normal>0 0 1</normal>
<size>{GROUND_SIZE} {GROUND_SIZE}</size>
</plane>
</geometry>
<material>
<ambient>0.8 0.8 0.8 1</ambient>
<diffuse>0.8 0.8 0.8 1</diffuse>
<specular>0.8 0.8 0.8 1</specular>
</material>
</visual>
<inertial>
<pose>0 0 0 0 0 0</pose>
<mass>1</mass>
<inertia>
<ixx>1</ixx>
<ixy>0</ixy>
<ixz>0</ixz>
<iyy>1</iyy>
<iyz>0</iyz>
<izz>1</izz>
</inertia>
</inertial>
<enable_wind>false</enable_wind>
</link>
<pose>0 0 0 0 0 0</pose>
<self_collide>false</self_collide>
</model>

'''
    
    # Generate positions based on layout
    positions = generate_positions()
    
    # Generate columns
    for i, (x, y) in enumerate(positions):
        z = COLUMN_HEIGHT / 2.0  # Half height to position base on ground
        
        # Gradual color variation
        if NUM_COLUMNS > 1:
            progress = i / (NUM_COLUMNS - 1)
        else:
            progress = 0
            
        r = 1.0 - progress * 0.7  # Red to purple
        g = 0.2 + progress * 0.6  # Dark to green
        b = 0.3 + progress * 0.7  # Dark to blue
        
        # Add column to SDF
        sdf_content += f'''
<!-- Column {i+1} -->
<model name="column_{i+1}">
<static>true</static>
<pose>{x:.2f} {y:.2f} {z:.2f} 0 0 0</pose>
<link name="link">
<visual name="visual">
<geometry>
<box>
<size>{COLUMN_WIDTH} {COLUMN_WIDTH} {COLUMN_HEIGHT}</size>
</box>
</geometry>
<material>
<ambient>{r:.2f} {g:.2f} {b:.2f} 1</ambient>
<diffuse>{r:.2f} {g:.2f} {b:.2f} 1</diffuse>
<specular>0.5 0.5 0.5 1</specular>
</material>
</visual>
<collision name="collision">
<geometry>
<box>
<size>{COLUMN_WIDTH} {COLUMN_WIDTH} {COLUMN_HEIGHT}</size>
</box>
</geometry>
</collision>
<inertial>
<pose>0 0 0 0 0 0</pose>
<mass>100</mass>
<inertia>
<ixx>52.08</ixx>
<ixy>0</ixy>
<ixz>0</ixz>
<iyy>52.08</iyy>
<iyz>0</iyz>
<izz>1.33</izz>
</inertia>
</inertial>
</link>
</model>
'''
    
    # SDF file footer
    sdf_content += '''
<!-- Lighting -->
<light name="sunUTC" type="directional">
<pose>0 0 500 0 0 0</pose>
<cast_shadows>true</cast_shadows>
<intensity>1</intensity>
<direction>0.001 0.625 -0.78</direction>
<diffuse>0.904 0.904 0.904 1</diffuse>
<specular>0.271 0.271 0.271 1</specular>
<attenuation>
<range>2000</range>
<linear>0</linear>
<constant>1</constant>
<quadratic>0</quadratic>
</attenuation>
<spot>
<inner_angle>0</inner_angle>
<outer_angle>0</outer_angle>
<falloff>0</falloff>
</spot>
</light>

<spherical_coordinates>
<surface_model>EARTH_WGS84</surface_model>
<world_frame_orientation>ENU</world_frame_orientation>
<latitude_deg>47.397971057728974</latitude_deg>
<longitude_deg> 8.546163739800146</longitude_deg>
<elevation>0</elevation>
</spherical_coordinates>
</world>
</sdf>
'''
    
    return sdf_content

def generate_positions():
    """
    Generate column positions based on selected layout
    """
    positions = []
    
    if LAYOUT == "line":
        # Columns in straight line
        for i in range(NUM_COLUMNS):
            x = START_X + i * SPACING
            y = 0
            positions.append((x, y))
            
    elif LAYOUT == "grid":
        # Columns in square grid
        cols = int(math.ceil(math.sqrt(NUM_COLUMNS)))
        rows = int(math.ceil(NUM_COLUMNS / cols))
        
        for i in range(NUM_COLUMNS):
            row = i // cols
            col = i % cols
            x = START_X + col * SPACING
            y = 0 + row * SPACING  # Start from Y=0
            positions.append((x, y))
            
    elif LAYOUT == "circle":
        # Columns arranged in circle
        radius = SPACING * NUM_COLUMNS / (2 * math.pi)
        if radius < SPACING:  # Minimum radius
            radius = SPACING * 2
            
        for i in range(NUM_COLUMNS):
            angle = 2 * math.pi * i / NUM_COLUMNS
            x = START_X + radius * math.cos(angle)
            y = 0 + radius * math.sin(angle)
            positions.append((x, y))
            
    elif LAYOUT == "random":
        # Random positions in area
        random.seed(42)  # For reproducible results
        area_width = NUM_COLUMNS * SPACING / 4  # Area proportional to number
        area_height = area_width
        
        for i in range(NUM_COLUMNS):
            x = START_X + random.uniform(0, area_width)
            y = random.uniform(-area_height/2, area_height/2)
            positions.append((x, y))
            
    else:
        print(f"Layout '{LAYOUT}' not recognized. Using 'line'.")
        return generate_positions_line()
    
    return positions

def print_summary():
    """
    Print configuration summary
    """
    print("PARAMETRIC COLUMN GENERATOR")
    print("=" * 50)
    print(f"Number of columns: {NUM_COLUMNS}")
    print(f"Spacing: {SPACING}m")
    print(f"Dimensions: {COLUMN_WIDTH}x{COLUMN_WIDTH}x{COLUMN_HEIGHT}m")
    print(f"Start X: {START_X}m")
    print(f"Layout: {LAYOUT}")
    print(f"World name: {WORLD_NAME}")
    print(f"Output file: {OUTPUT_FILE}")
    
    if LAYOUT == "line":
        end_x = START_X + (NUM_COLUMNS - 1) * SPACING
        print(f"Occupied area: X from {START_X}m to {end_x:.1f}m, Y=0m")
    elif LAYOUT == "grid":
        cols = int(math.ceil(math.sqrt(NUM_COLUMNS)))
        rows = int(math.ceil(NUM_COLUMNS / cols))
        end_x = START_X + (cols - 1) * SPACING
        end_y = (rows - 1) * SPACING
        print(f"Grid: {cols}x{rows}, Area: X={START_X}-{end_x:.1f}m, Y=0-{end_y:.1f}m")
    elif LAYOUT == "circle":
        radius = SPACING * NUM_COLUMNS / (2 * math.pi)
        if radius < SPACING * 2:
            radius = SPACING * 2
        print(f"Circle: center=({START_X:.1f}, 0), radius={radius:.1f}m")
    elif LAYOUT == "random":
        area_width = NUM_COLUMNS * SPACING / 4
        area_height = area_width
        print(f"Random area: X={START_X:.1f} to {START_X + area_width:.1f}m, Y={-area_height/2:.1f} to {area_height/2:.1f}m")

if __name__ == "__main__":
    print_summary()
    print("\nGenerating SDF file...")
    
    # Generate SDF file
    sdf_content = generate_columns_sdf()
    
    # Save file
    with open(OUTPUT_FILE, 'w') as f:
        f.write(sdf_content)
    
    print(f"File generated: {OUTPUT_FILE}")
    
    # Useful warnings
    if NUM_COLUMNS > 500:
        print("WARNING: Many columns might slow down Gazebo!")
    
    if LAYOUT == "line" and NUM_COLUMNS > 50:
        end_x = START_X + (NUM_COLUMNS - 1) * SPACING
        print(f"Columns extend to X={end_x:.1f}m")
        
