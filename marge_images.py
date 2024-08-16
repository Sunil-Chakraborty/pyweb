from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def optimize_image(image, max_width, max_height, quality=85, img_name=""):
    """Resize and compress image."""
    # Calculate the scaling factor to fit the image to the desired size
    img_width, img_height = image.size
    scale = min(max_width / img_width, max_height / img_height)

    # Calculate new image dimensions
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)

    # Resize the image
    optimized_img = image.resize((new_width, new_height), Image.LANCZOS)

    # Use a unique temporary file name for each image
    temp_img_path = f"temp_optimized_{img_name}.jpg"
    optimized_img.save(temp_img_path, "JPEG", quality=quality, optimize=True)

    return temp_img_path

def images_to_pdf(image_paths, output_path, max_width=600, max_height=800, quality=85):
    """Convert a list of images to a PDF with specified maximum dimensions and compression quality."""
    # Create a canvas for the PDF
    pdf = canvas.Canvas(output_path, pagesize=letter)

    for img_path in image_paths:
        try:
            # Open the image
            img = Image.open(img_path)

            # Debugging statement: Print the current image being processed
            print(f"Processing image: {img_path}")

            # Extract the base name of the image file for unique naming
            img_name = os.path.basename(img_path).split('.')[0]

            # Optimize image
            temp_img_path = optimize_image(img, max_width, max_height, quality, img_name)

            # Draw the optimized image on the PDF, centered on the page
            pdf.drawImage(temp_img_path, 0, 0, width=max_width, height=max_height)

            # Add a new page for the next image
            pdf.showPage()

            # Delete the temporary image file after it's drawn on the PDF
            os.remove(temp_img_path)

        except IOError as e:
            print(f"Error processing image {img_path}: {e}")

    # Save the PDF
    pdf.save()
    print(f"PDF saved to {output_path}")

# Define the paths
image_paths = [
    r'D:\PyWeb\rh5.jpg',
    r'D:\PyWeb\rh6.jpg',
    r'D:\PyWeb\rh8.jpg',
    r'D:\PyWeb\rh9.jpg'
]  # Add all your source image paths here

output_path = r'D:\PyWeb\merged_images.pdf'

# Call the function with maximum size parameters and desired quality
images_to_pdf(image_paths, output_path, max_width=600, max_height=800, quality=85)
