import OpenEXR
import Imath
import numpy as np

# Define image size (2x2)
width, height = 2, 2

# Define OpenEXR pixel type (32-bit float per channel)
FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)

# Create the 1-channel grayscale image data (stored row-major)
data = np.array([2, 1, 1, 2], dtype=np.float32).reshape(height, width)

data_bytes = data.tobytes()  # Convert to raw binary format

# Create an OpenEXR header
header = OpenEXR.Header(width, height)
header['channels'] = {'Y': Imath.Channel(FLOAT)}  # Define a single-channel grayscale image

# DEBUG: Print header to check correctness
print("Header created successfully:", header)

# Try writing the file
try:
    exr_file = OpenEXR.OutputFile("texture_full_2.exr", header)
    exr_file.writePixels({'Y': data_bytes})  # Writing the grayscale data
    exr_file.close()
    print("OpenEXR file saved successfully.")
except Exception as e:
    print("Error creating OpenEXR file:", e)