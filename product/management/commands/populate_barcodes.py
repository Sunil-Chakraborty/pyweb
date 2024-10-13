# barcode_populate/management/commands/populate_barcodes.py
from django.core.management.base import BaseCommand
from product.models import RawMat  # Make sure the import matches your app structure
import barcode
from barcode.writer import ImageWriter

class Command(BaseCommand):
    help = 'Populates barcode field for all existing RawMat records'

    def handle(self, *args, **kwargs):
        # Loop through all RawMat records
        for raw_mat in RawMat.objects.all():
            # Generate a barcode from the rm_cd (or any other field)
            barcode_class = barcode.get_barcode_class('code128')
            barcode_obj = barcode_class(str(raw_mat.rm_cd), writer=ImageWriter())
            
            # You can save the code (as a string) instead of an image here
            barcode_string = barcode_obj.get_fullcode()

            # Populate the barcode field
            raw_mat.barcode = barcode_string
            raw_mat.save()

            self.stdout.write(self.style.SUCCESS(f"Updated barcode for {raw_mat.rm_cd}"))
