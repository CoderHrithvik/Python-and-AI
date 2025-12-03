import cv2
import matplotlib.pyplot as plt

# Step 1: Load the Image
  # User-provided image path

# Convert BGR to RGB for correct color display with matplotlib

# Get image dimensions

# Step 2: Draw Two Rectangles Around Interesting Regions
# Rectangle 1: Top-left corner
  # Fixed 20 pixels padding from top-left
# Yellow rectangle

# Rectangle 2: Bottom-right corner
  # 20 pixels padding
  # Magenta rectangle

# Step 3: Draw Circles at the Centers of Both Rectangles
   # Filled green circle
    # Filled red circle

# Step 4: Draw Connecting Lines Between Centers of Rectangles


# Step 5: Add Text Labels for Regions and Centers


# Step 6: Add Bi-Directional Arrow Representing Height
  # Start near the top-right
  # End near the bottom-right

# Draw arrows in both directions
  # Downward arrow
 # Upward arrow

# Annotate the height value


# Step 7: Display the Annotated Image
