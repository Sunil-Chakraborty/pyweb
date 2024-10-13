from barcode import get_barcode_class
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import os
from django.core.management.base import BaseCommand
from product.models import RawMat  # Import your RawMat model

class Command(BaseCommand):
    help = 'Generates barcodes with additional information for all raw materials'

    def handle(self, *args, **kwargs):
        self.generate_barcodes()

    def generate_barcodes(self):
        for raw_mat in RawMat.objects.all():
            # Log the action
            self.stdout.write(f"Generating barcode for {raw_mat.rm_des} - {raw_mat.rm_cd}")
            # Call the method to save the barcode
            self.save_barcode_with_info(raw_mat)

    def save_barcode_with_info(self, raw_mat):
        # Ensure the 'barcodes' directory exists
        barcode_dir = os.path.join(settings.MEDIA_ROOT, 'barcodes')
        if not os.path.exists(barcode_dir):
            os.makedirs(barcode_dir)

        # Generate the barcode image
        barcode_class = get_barcode_class('code128')
        barcode_obj = barcode_class(str(raw_mat.rm_cd), writer=ImageWriter())

        # Save the barcode image without manually appending '.png'
        barcode_image_path = os.path.join(barcode_dir, raw_mat.rm_cd)  # No need to append '.png'
        
        saved_file = barcode_obj.save(barcode_image_path)  # 'save()' method automatically adds .png

        # Open the saved barcode image using Pillow
        barcode_image = Image.open(f"{saved_file}.png")
        draw = ImageDraw.Draw(barcode_image)

        # Define font size and type (adjust path and size as needed)
        font_path = os.path.join(settings.MEDIA_ROOT, 'fonts', 'arial.ttf')  # Path to the font file
        font = ImageFont.truetype(font_path, 20)

        # Prepare the text to overlay
        text = f"RM Code: {raw_mat.rm_cd}\nRM Description: {raw_mat.rm_des}\nRate: {raw_mat.rate} Rs/Kg"
        
        # Define the position for the text (top left corner)
        text_position = (10, barcode_image.height + 10)

        # Resize the image to make room for the text if needed
        new_height = barcode_image.height + 80  # Adjust the height based on text size
        new_image = Image.new('RGB', (barcode_image.width, new_height), (255, 255, 255))  # Create a white background
        new_image.paste(barcode_image, (0, 0))  # Paste the barcode image onto the white background

        # Add text to the new image
        draw = ImageDraw.Draw(new_image)
        draw.text(text_position, text, font=font, fill=(0, 0, 0))

        # Save the final image with text and barcode
        final_image_path = os.path.join(barcode_dir, f"{raw_mat.rm_cd}.png")  # Save final image with .png
        new_image.save(final_image_path)

        print(f"Final image saved to: {final_image_path}")
        return final_image_path
