import barcode
from barcode.writer import ImageWriter

# Choose the barcode format (e.g., Code128)
barcode_class = barcode.get_barcode_class('code128')

# Create the barcode object with data and writer
barcode_data = barcode_class('1234567890', writer=ImageWriter())

# Save the barcode as a PNG image
filename = barcode_data.save('barcode_image')

print(f"Barcode saved as {filename}.png")
