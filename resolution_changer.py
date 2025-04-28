from PIL import Image

# Open the image
img = Image.open("uploads/shifted_reality.png")

# Define the new dimensions (width, height)
new_dimensions = (3456, 3210)

# Resize the image
resized_img = img.resize(new_dimensions, P.Image)

# Define the new DPI (e.g., 300 DPI for high resolution)
new_dpi = (3456, 3210)

# Save the resized image with the new DPI
resized_img.save("resized_image.png", dpi=new_dpi)

# Optionally, show the resized image
resized_img.show()
