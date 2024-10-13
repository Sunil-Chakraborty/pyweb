import barcode
from barcode.writer import ImageWriter
import os
from product.models import RawMat

def save_all_barcodes():
    # Ensure the 'barcodes' directory exists
    barcode_dir = r'D:\PyWeb\media\barcodes'
    if not os.path.exists(barcode_dir):
        os.makedirs(barcode_dir)

    # Loop through all raw materials and generate their barcodes
    for raw_mat in RawMat.objects.all():
        barcode_class = barcode.get_barcode_class('code128')
        barcode_obj = barcode_class(str(raw_mat.rm_cd), writer=ImageWriter())

        # Save the barcode image
        filename = os.path.join(barcode_dir, f'{raw_mat.rm_cd}.png')
        print(f"Saving barcode for {raw_mat.rm_des} - {raw_mat.rm_cd} to: {filename}")
        barcode_obj.save(filename)

# Call the function to generate barcodes for all RawMat entries
save_all_barcodes()
