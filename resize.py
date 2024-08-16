from PIL import Image

# Open the image
image = Image.open("D:/PyWeb/sunil.png")

# Resize the image
image = image.resize((100, 125), Image.LANCZOS)

# Save the resized image
image.save("D:/PyWeb/sunil_resized.png")
